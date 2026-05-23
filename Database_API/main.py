import os
import random
import smtplib
import threading
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Optional, List
from dotenv import load_dotenv
import asyncio
import mysql.connector
import json
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# ---------- SMS SENDING FUNCTION ----------
def send_sms_otp(phone_number: str, otp_code: str) -> bool:
    """
    Send OTP via SMS using Twilio.
    Returns True if SMS was sent successfully, False otherwise.
    """
    try:
        # Check if Twilio is configured
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            print("[SMS] Twilio not configured")
            return False
        
        # Import Twilio client
        from twilio.rest import Client
        
        # Create Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send SMS
        message_body = f"Your OTP verification code is: {otp_code}\n\nThis code will expire in {OTP_TTL_MINUTES} minutes."
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        print(f"✅ SMS OTP sent successfully to {phone_number}")
        return True
        
    except ImportError:
        print("❌ Twilio library not installed")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error sending SMS: {error_msg}")
        
        # Provide specific guidance for common Twilio trial account issues
        if "21408" in error_msg or "Permission to send an SMS has not been enabled" in error_msg:
            print("🔧 Twilio Trial Account Limitation:")
            print("   - In trial mode, you can only send SMS to verified numbers")
            print("   - Make sure the recipient number is verified in your Twilio console")
            print("   - Go to Twilio Console > Phone Numbers > Verified Caller IDs")
            print("   - Format the number correctly with country code (e.g., +1234567890)")
        elif "21211" in error_msg or "not a valid phone number" in error_msg:
            print("🔧 Phone Number Format Issue:")
            print("   - Make sure the phone number includes the country code")
            print("   - Example format: +1234567890 (for US/Canada)")
        
        return False

# FastAPI app
app = FastAPI()

# CORS middleware - Updated to be more explicit and allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    allow_origin_regex=None
)

# Configuration from environment variables
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME) or SMTP_USERNAME or "noreply@example.com"
OTP_TTL_MINUTES = int(os.getenv("EMAIL_OTP_TTL_MINUTES", "10"))
OTP_DEBUG = os.getenv("OTP_DEBUG", "false").lower() == "true"

# Ensure we're using the correct environment variables
if not SMTP_USERNAME:
    SMTP_USERNAME = os.getenv("EMAIL_USERNAME", "")
if not SMTP_PASSWORD:
    SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# In-memory storage for OTPs (in production, use Redis or database)
otp_store: Dict[str, Dict] = {}

# ---------- EMAIL SENDING FUNCTION ----------
def send_email_otp(email: str, otp_code: str) -> bool:
    """
    Send OTP via email using Gmail SMTP with proper error handling.
    Returns True if email was sent successfully, False otherwise.
    """
    try:
        if not EMAIL_ENABLED:
            return False
        
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = "Your OTP Code for Voting System"
        
        body = f"""Hello,

Your OTP verification code is: {otp_code}

This code will expire in {OTP_TTL_MINUTES} minutes.

If you did not request this code, please ignore this email.

Thank you,
Voting System Team"""
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session with timeout
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        
        # Enable TLS encryption with specific context for Gmail
        import ssl
        context = ssl.create_default_context()
        server.starttls(context=context)
        
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SMTP_FROM_EMAIL, email, text)
        server.quit()
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        return False
    except smtplib.SMTPRecipientsRefused as e:
        return False
    except smtplib.SMTPServerDisconnected as e:
        return False
    except smtplib.SMTPConnectError as e:
        return False
    except smtplib.SMTPHeloError as e:
        return False
    except smtplib.SMTPSenderRefused as e:
        return False
    except smtplib.SMTPException as e:
        return False
    except Exception as e:
        return False

# ---------- ASYNC EMAIL SENDING FUNCTION ----------
def send_email_otp_async(email: str, otp_code: str):
    """
    Send OTP via email asynchronously using threading.
    This prevents blocking the main thread during email sending.
    """
    def send_email_thread():
        try:
            send_email_otp(email, otp_code)
        except Exception as e:
            print(f"Error in email sending thread: {e}")
    
    # Start email sending in a separate thread
    email_thread = threading.Thread(target=send_email_thread, daemon=True)
    email_thread.start()

# Pydantic models for request validation
class OtpRequest(BaseModel):
    email: Optional[str] = None
    contact_number: Optional[str] = None

class OtpVerifyRequest(BaseModel):
    email: Optional[str] = None
    contact_number: Optional[str] = None
    otp: str

# ---------- OTP SEND ----------
@app.get("/otp/send")
async def send_otp_get():
    # OTP send endpoint (GET) - not allowed
    raise HTTPException(status_code=405, detail="Method Not Allowed: Use POST method instead of GET for sending OTP")

@app.post("/otp/send")
async def send_otp(payload: OtpRequest):
    # OTP send endpoint
    
    try:
        # Extract values from Pydantic model
        contact_number = payload.contact_number
        email = payload.email
        
        if not contact_number and not email:
            raise HTTPException(status_code=400, detail="Either contact_number or email is required")
        
        if contact_number and email:
            raise HTTPException(status_code=400, detail="Provide either contact_number or email, not both")
        
        # Generate a 6-digit OTP
        otp_code = f"{random.randint(0, 999999):06d}"
        
        expires_at = datetime.utcnow() + timedelta(minutes=OTP_TTL_MINUTES)
        
        if contact_number:
            # Phone OTP validation
            # Ensure phone number is properly formatted for Twilio (E.164 format)
            if contact_number.startswith('0'):
                # If it starts with 0, assume it's missing country code
                print(f"⚠️  Phone number {contact_number} might be missing country code")
            elif not contact_number.startswith('+'):
                # If it doesn't start with +, it might be missing country code
                print(f"⚠️  Phone number {contact_number} might be missing country code (+ prefix)")
            
            # Basic validation for phone number format
            if not contact_number.isdigit() and not (contact_number.startswith('+') and contact_number[1:].isdigit()):
                raise HTTPException(status_code=400, detail="Invalid phone number format. Use E.164 format (e.g., +1234567890)")
            
            # Length validation (E.164 format is typically 7-15 digits)
            clean_number = contact_number.lstrip('+')
            if len(clean_number) < 7 or len(clean_number) > 15:
                raise HTTPException(status_code=400, detail="Invalid phone number length. Use E.164 format (e.g., +1234567890)")
            
            otp_store[contact_number] = {
                "otp": otp_code,
                "expires_at": expires_at,
                "verified_until": None,
                "attempts": 0,
                "type": "phone"
            }
            
            # Send SMS OTP
            sms_sent = send_sms_otp(contact_number, otp_code)
            if not sms_sent:
                # Even if SMS sending failed, we still return success because the OTP was generated
                # But we log the failure for debugging
                print(f"⚠️  SMS sending failed for {contact_number}, but OTP is stored in memory")
            
        elif email:
            # Email OTP validation
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise HTTPException(status_code=400, detail="Invalid email format")
            
            otp_store[email] = {
                "otp": otp_code,
                "expires_at": expires_at,
                "verified_until": None,
                "attempts": 0,
                "type": "email"
            }
            
            # Send email OTP asynchronously to prevent blocking
            send_email_otp_async(email, otp_code)
        else:
            print("ERROR: Neither email nor contact_number provided!")
        
        response = {"success": True, "message": "OTP sent"}
        # Only include OTP in development mode (when email/SMS not configured)
        # Show dev_otp when OTP_DEBUG is enabled, regardless of EMAIL_ENABLED
        if OTP_DEBUG:
            response["dev_otp"] = otp_code
            if EMAIL_ENABLED and email:
                response["note"] = "Development mode: OTP shown for testing. Email was attempted."
            elif TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER and contact_number:
                response["note"] = "Development mode: OTP shown for testing. SMS was attempted."
            else:
                response["note"] = "Development mode: OTP shown for testing. Email/SMS not configured."
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error in send_otp: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

# ---------- OTP VERIFY ----------
@app.post("/otp/verify")
async def verify_otp(payload: OtpVerifyRequest):
    # OTP verification endpoint
    
    contact_number = payload.contact_number
    email = payload.email
    otp = payload.otp
    
    identifier = email or contact_number
    
    if not identifier:
        raise HTTPException(status_code=400, detail="Email or contact number required")
    
    if not otp:
        raise HTTPException(status_code=400, detail="OTP required")
    
    # Check if OTP exists
    if identifier not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not found or expired")
    
    stored_otp_data = otp_store[identifier]
    
    # Check if OTP is expired
    if datetime.utcnow() > stored_otp_data["expires_at"]:
        del otp_store[identifier]  # Clean up expired OTP
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Check if already verified
    if stored_otp_data["verified_until"] and datetime.utcnow() < stored_otp_data["verified_until"]:
        return {"success": True, "message": "OTP verified"}
    
    # Check attempts
    if stored_otp_data["attempts"] >= 5:  # Max 5 attempts
        del otp_store[identifier]  # Clean up after too many attempts
        raise HTTPException(status_code=400, detail="Too many failed attempts. Request a new OTP.")
    
    # Verify OTP
    if stored_otp_data["otp"] == otp:
        # Mark as verified for 10 minutes
        stored_otp_data["verified_until"] = datetime.utcnow() + timedelta(minutes=10)
        stored_otp_data["attempts"] = 0  # Reset attempts on success
        return {"success": True, "message": "OTP verified"}
    else:
        # Increment attempts
        stored_otp_data["attempts"] += 1
        raise HTTPException(status_code=400, detail="Invalid OTP")

# ---------- LOGIN ----------
@app.get("/login")
async def login(email: str, password: str):
    """
    Login endpoint for admin and user authentication
    """
    print("=" * 50)
    print("LOGIN ENDPOINT HIT!")
    print("=" * 50)
    print(f"=== /login endpoint called ===")
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    
    try:
        # Import database connection
        from dotenv import load_dotenv
        import os
        import bcrypt
        
        # Load environment variables
        load_dotenv(dotenv_path="../.env")
        load_dotenv()  # Also load from current directory
        
        # Debug: Print database credentials
        print(f"[DB_DEBUG] MYSQL_USER: {os.environ.get('MYSQL_USER', 'NOT SET')}")
        print(f"[DB_DEBUG] MYSQL_PASSWORD: {'*' * len(os.environ.get('MYSQL_PASSWORD', '')) if os.environ.get('MYSQL_PASSWORD') else 'EMPTY'}")
        print(f"[DB_DEBUG] MYSQL_HOST: {os.environ.get('MYSQL_HOST', 'NOT SET')}")
        print(f"[DB_DEBUG] MYSQL_DB: {os.environ.get('MYSQL_DB', 'NOT SET')}")
        
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Query user by email
        query = "SELECT firstName, lastName, emailid, password, role FROM users WHERE emailid = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        cursor.close()
        cnx.close()
        
        if user:
            # User found, check password
            first_name, last_name, user_email, stored_password, role = user
            
            # Verify password (currently stored as plain text)
            # In production, use bcrypt: bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            if stored_password != password:
                print(f"❌ Password mismatch for user: {user_email}")
                print(f"   Stored password: {stored_password}")
                print(f"   Provided password: {password}")
                cursor.close()
                cnx.close()
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            print(f"✅ User found and password verified: {first_name} {last_name} ({role})")
            
            # Generate a simple token (in production, use JWT)
            import jwt
            import time
            token = jwt.encode({
                'email': email,
                'role': role,
                'exp': time.time() + 3600  # 1 hour expiration
            }, os.environ.get('SECRET_KEY', 'fallback_secret_key'), algorithm='HS256')
            
            return {
                "success": True,
                "token": token,
                "role": role,
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": user_email,
                    "role": role
                }
            }
        else:
            print("❌ User not found")
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# ---------- REGISTRATION ----------
class RegistrationRequest(BaseModel):
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    email: str
    aadhar: Optional[str] = None
    voterId: str
    dob: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contactNumber: str
    address: Optional[str] = None
    password: str
    confirmPassword: Optional[str] = None

# Import our safe registration function
from safe_register import safe_register

@app.post("/register")
async def register(payload: RegistrationRequest):
    # Use our safe registration function that matches your exact table structure
    return safe_register(payload)

# Helper function to get database connection
def get_db_connection():
    from dotenv import load_dotenv
    import os
    
    # Load environment variables
    load_dotenv(dotenv_path="../.env")
    load_dotenv()  # Also load from current directory
    
    # Debug: Print database credentials (masked)
    print(f"[DB_DEBUG] MYSQL_USER: {os.environ.get('MYSQL_USER', 'NOT SET')}")
    print(f"[DB_DEBUG] MYSQL_PASSWORD: {'*' * len(os.environ.get('MYSQL_PASSWORD', '')) if os.environ.get('MYSQL_PASSWORD') else 'EMPTY'}")
    print(f"[DB_DEBUG] MYSQL_HOST: {os.environ.get('MYSQL_HOST', 'NOT SET')}")
    print(f"[DB_DEBUG] MYSQL_DB: {os.environ.get('MYSQL_DB', 'NOT SET')}")
    
    # Check if all required environment variables are set
    required_vars = ['MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_DB']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise Exception(f"Missing required environment variables: {missing_vars}")
    
    # Connect to database
    try:
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        print("✅ Database connection successful")
        return cnx
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        raise Exception(f"Database connection failed: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected database connection error: {e}")
        raise Exception(f"Database connection error: {str(e)}")

# ---------- CANDIDATE MANAGEMENT ----------
# Import required modules for candidate management
import json
from fastapi import File, UploadFile, Form
from typing import List

# Pydantic models for candidate management
class Candidate(BaseModel):
    id: int
    name: str
    party: str
    photo_hash: str = ""
    party_logo_hash: str = ""

# Get all candidates
@app.get("/candidates")
async def get_candidates():
    print("=" * 50)
    print("GET CANDIDATES ENDPOINT HIT!")
    print("=" * 50)
    
    try:
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        
        # Query all candidates
        query = "SELECT id, name, party, photo_hash as photo FROM candidates"
        cursor.execute(query)
        candidates = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        return candidates
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Add a new candidate
@app.post("/candidates")
async def add_candidate(
    name: str = Form(...),
    party: str = Form(...),
    photo: UploadFile = File(None)
):
    print("=" * 50)
    print("ADD CANDIDATE ENDPOINT HIT!")
    print("=" * 50)
    print(f"Name: {name}")
    print(f"Party: {party}")
    
    try:
        # Handle photo upload (simplified for now)
        photo_hash = ""
        party_logo_hash = ""
        if photo:
            # In a real implementation, you would save the file and generate a hash
            # For now, we'll just note that a photo was provided
            photo_hash = f"hash_{name.replace(' ', '_')}"  # Simplified
            print(f"Photo provided: {photo.filename}")
        
        # Validate inputs
        if not name or not party:
            raise HTTPException(status_code=400, detail="Name and party are required")
        
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Insert new candidate
        query = "INSERT INTO candidates (name, party, photo_hash, party_logo_hash) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, party, photo_hash, party_logo_hash))
        cnx.commit()
        
        # Get the ID of the inserted candidate
        candidate_id = cursor.lastrowid
        
        cursor.close()
        cnx.close()
        
        return {
            "success": True,
            "id": candidate_id,
            "name": name,
            "party": party,
            "photo": photo_hash
        }
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        # Re-raise HTTP exceptions
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Delete a candidate
@app.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int):
    print("=" * 50)
    print("DELETE CANDIDATE ENDPOINT HIT!")
    print("=" * 50)
    print(f"Candidate ID: {candidate_id}")
    
    try:
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Delete candidate
        query = "DELETE FROM candidates WHERE id = %s"
        cursor.execute(query, (candidate_id,))
        cnx.commit()
        
        # Check if any rows were affected
        if cursor.rowcount == 0:
            cursor.close()
            cnx.close()
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        cursor.close()
        cnx.close()
        
        return {"success": True, "message": "Candidate deleted successfully"}
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        # Re-raise HTTP exceptions
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # Ensure we close connections even in error cases
        try:
            cursor.close()
            cnx.close()
        except:
            pass
        # Return a proper JSON error response
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Pydantic model for voting dates
class VotingDates(BaseModel):
    startDate: str
    endDate: str
    resultDate: str
    resultMessage: str

# Get voting dates
@app.get("/voting-dates")
async def get_voting_dates():
    print("=" * 50)
    print("GET VOTING DATES ENDPOINT HIT!")
    print("=" * 50)
    
    try:
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Query voting dates
        query = "SELECT start_date, end_date, result_date, result_message FROM voting_dates ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        dates = cursor.fetchone()
        
        cursor.close()
        cnx.close()
        
        if dates:
            # Convert datetime objects to ISO format strings
            result = {}
            start_date, end_date, result_date, result_message = dates
            
            # Convert to string and handle None values
            if start_date:
                result['startDate'] = str(start_date)
            if end_date:
                result['endDate'] = str(end_date)
            if result_date:
                result['resultDate'] = str(result_date)
            if result_message:
                result['resultMessage'] = result_message
            
            return result
        else:
            return {}
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Set voting dates
@app.post("/voting-dates")
async def set_voting_dates(dates: VotingDates):
    print("=" * 50)
    print("SET VOTING DATES ENDPOINT HIT!")
    print("=" * 50)
    print(f"Dates: {dates}")
    
    try:
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Insert or update voting dates
        query = """
            INSERT INTO voting_dates (start_date, end_date, result_date, result_message) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            start_date = VALUES(start_date), 
            end_date = VALUES(end_date), 
            result_date = VALUES(result_date), 
            result_message = VALUES(result_message)
        """
        
        # Convert ISO format strings to datetime objects
        from datetime import datetime
        start_date = datetime.fromisoformat(dates.startDate.replace('Z', '+00:00')) if dates.startDate else None
        end_date = datetime.fromisoformat(dates.endDate.replace('Z', '+00:00')) if dates.endDate else None
        result_date = datetime.fromisoformat(dates.resultDate.replace('Z', '+00:00')) if dates.resultDate else None
        
        cursor.execute(query, (start_date, end_date, result_date, dates.resultMessage))
        cnx.commit()
        
        cursor.close()
        cnx.close()
        
        return {"success": True, "message": "Voting dates updated successfully"}
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Pydantic model for voting
class VoteRequest(BaseModel):
    candidateId: int

# Import the vote function from voting_api
try:
    from voting_api import vote
    VOTING_API_AVAILABLE = True
    print("✅ Voting API imported successfully")
except ImportError as e:
    print(f"⚠️  Voting API import failed: {e}")
    print("   System will work in database-only mode")
    
    # Create a dummy vote function for when voting_api is not available
    def vote(candidate_id, voter_id):
        return {
            "success": True,
            "transaction_hash": "0x" + "0" * 64  # Dummy hash
        }
    VOTING_API_AVAILABLE = False

# Cast vote
@app.post("/vote")
async def cast_vote(vote_request: VoteRequest, authorization: str = Header(None)):
    print("=" * 50)
    print("CAST VOTE ENDPOINT HIT!")
    print("=" * 50)
    print(f"Candidate ID: {vote_request.candidateId}")
    print(f"Authorization: {authorization}")
    
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Decode token to get user info
        import jwt
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        try:
            secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
            print(f"[DEBUG] SECRET_KEY from env: {secret_key[:10]}...")  # Log only first 10 chars for security
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_email = decoded.get('email')
            print(f"User email from token: {user_email}")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"Invalid token error: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(f"Token decoding error: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Connect to database
        try:
            cnx = get_db_connection()
            print("✅ Database connection established")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
        
        try:
            # Get user details using dictionary cursor
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT voterId, has_voted FROM users WHERE emailid = %s"
            cursor.execute(query, (user_email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                cnx.close()
                raise HTTPException(status_code=404, detail="User not found")
            
            # Access dictionary values correctly
            voter_id = user['voterId']
            has_voted = user['has_voted']
            print(f"User details - Voter ID: {voter_id}, Has voted: {has_voted}")
            
            # Check if user has already voted
            if has_voted:
                cursor.close()
                cnx.close()
                raise HTTPException(status_code=400, detail="You have already voted")
            
            # Check if candidate exists with regular cursor
            cursor = cnx.cursor()
            query = "SELECT id FROM candidates WHERE id = %s"
            cursor.execute(query, (vote_request.candidateId,))
            candidate = cursor.fetchone()
            
            if not candidate:
                cursor.close()
                cnx.close()
                raise HTTPException(status_code=404, detail="Candidate not found")
            
            print(f"Candidate {vote_request.candidateId} found")
            
            # Cast vote using voting API (or database-only if voting API unavailable)
            print("Calling vote function")
            if VOTING_API_AVAILABLE:
                print("Using voting API")
            else:
                print("Using fallback voting function (database-only mode)")
                
            result = vote(vote_request.candidateId, voter_id)
            print(f"Vote function result: {result}")
            
            if "error" in result:
                cursor.close()
                cnx.close()
                raise HTTPException(status_code=500, detail=result["error"])
            
            # Update user's has_voted status in database
            print("Updating user's has_voted status")
            query = "UPDATE users SET has_voted = 1 WHERE emailid = %s"
            cursor.execute(query, (user_email,))
            
            # Increment candidate vote count in database
            print("Incrementing candidate vote count")
            query = "UPDATE candidates SET vote_count = COALESCE(vote_count, 0) + 1 WHERE id = %s"
            cursor.execute(query, (vote_request.candidateId,))
            
            cnx.commit()
            print("Database changes committed")
            
            cursor.close()
            cnx.close()
            
            return {"success": True, "message": "Vote cast successfully", "transaction_hash": result.get("transaction_hash")}
            
        except mysql.connector.Error as e:
            print(f"❌ Database error: {e}")
            # Ensure we close connections even in error cases
            try:
                cursor.close()
                cnx.close()
            except:
                pass
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except HTTPException:
            # Re-raise HTTP exceptions
            # Ensure we close connections even in error cases
            try:
                cursor.close()
                cnx.close()
            except:
                pass
            raise
        except Exception as e:
            print(f"❌ Unexpected error during voting process: {e}")
            import traceback
            traceback.print_exc()
            # Ensure we close connections even in error cases
            try:
                cursor.close()
                cnx.close()
            except:
                pass
            raise HTTPException(status_code=500, detail=f"Internal server error during voting: {str(e)}")
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error in cast_vote function: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Serve HTML files
import os
from fastapi.responses import HTMLResponse, FileResponse

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    file_path = "../src/html/index.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(content="<h1>Page not found</h1>", status_code=404)

# Test endpoint
@app.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint working"}

# Simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK"}

# Root path redirect to admin page
@app.get("/")
async def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin.html")

# Get election results (for admin dashboard)
@app.get("/api/results")
async def get_results_admin(authorization: str = Header(None)):
    print("=" * 50)
    print("GET RESULTS ENDPOINT HIT (ADMIN)!")
    print("=" * 50)
    print(f"Authorization: {authorization}")
    
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Decode token to verify it's valid
        import jwt
        from dotenv import load_dotenv
        import os
        # Load environment variables
        load_dotenv(dotenv_path="../.env")
        load_dotenv()  # Also load from current directory
        
        # Debug: Print SECRET_KEY
        secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
        print(f"[DEBUG] SECRET_KEY from env: {secret_key}")
        print(f"[DEBUG] Token: {token}")
        
        try:
            print(f"[DEBUG] Attempting to decode token with secret key: {secret_key}")
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_role = decoded.get('role')
            
            print(f"[DEBUG] Decoded token: {decoded}")
            print(f"[DEBUG] User role: {user_role}")
            
            # Check if user is admin
            if user_role != 'admin':
                raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        except jwt.ExpiredSignatureError as e:
            print(f"[DEBUG] Token expired: {e}")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(f"[DEBUG] Unexpected error during token decoding: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Query all candidates with vote counts
        query = "SELECT id, name, party, COALESCE(vote_count, 0) as vote_count FROM candidates ORDER BY vote_count DESC"
        cursor.execute(query)
        candidates_rows = cursor.fetchall()
        
        # Convert rows to dictionaries for proper JSON serialization
        candidates = []
        for row in candidates_rows:
            candidate_dict = {
                "id": row[0],
                "name": row[1],
                "party": row[2],
                "vote_count": row[3]
            }
            candidates.append(candidate_dict)
        
        # Get voting dates (handle case when table doesn't exist)
        dates_result = None
        try:
            query = "SELECT start_date, end_date, result_date, result_message FROM voting_dates ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            dates_result = cursor.fetchone()
        except mysql.connector.Error as e:
            if e.errno == 1146:  # Table doesn't exist
                print("⚠️  voting_dates table doesn't exist, continuing without dates")
                dates_result = None
            else:
                raise  # Re-raise if it's a different error
        
        cursor.close()
        cnx.close()
        
        # Prepare response with voting dates
        response_data = {"candidates": candidates}
        if dates_result:
            start_date, end_date, result_date, result_message = dates_result
            if result_date:
                response_data["resultDate"] = result_date.isoformat() if hasattr(result_date, 'isoformat') else str(result_date)
            if result_message:
                response_data["resultMessage"] = result_message
        
        return response_data
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get election results (for user dashboard)
@app.get("/api/user/results")
async def get_results_user(authorization: str = Header(None)):
    print("=" * 50)
    print("GET RESULTS ENDPOINT HIT (USER)!")
    print("=" * 50)
    print(f"Authorization: {authorization}")
    
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Decode token to verify it's valid (no role check for users)
        import jwt
        from dotenv import load_dotenv
        import os
        # Load environment variables
        load_dotenv(dotenv_path="../.env")
        load_dotenv()  # Also load from current directory
        
        # Debug: Print SECRET_KEY
        secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
        print(f"[DEBUG] SECRET_KEY from env: {secret_key}")
        print(f"[DEBUG] Token: {token}")
        
        try:
            print(f"[DEBUG] Attempting to decode token with secret key: {secret_key}")
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_role = decoded.get('role')
            
            print(f"[DEBUG] Decoded token: {decoded}")
            print(f"[DEBUG] User role: {user_role}")
        except jwt.ExpiredSignatureError as e:
            print(f"[DEBUG] Token expired: {e}")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(f"[DEBUG] Unexpected error during token decoding: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Query all candidates with vote counts
        query = "SELECT id, name, party, COALESCE(vote_count, 0) as vote_count FROM candidates ORDER BY vote_count DESC"
        cursor.execute(query)
        candidates_rows = cursor.fetchall()
        
        # Convert rows to dictionaries for proper JSON serialization
        candidates = []
        for row in candidates_rows:
            candidate_dict = {
                "id": row[0],
                "name": row[1],
                "party": row[2],
                "vote_count": row[3]
            }
            candidates.append(candidate_dict)
        
        # Get voting dates (handle case when table doesn't exist)
        dates_result = None
        try:
            query = "SELECT start_date, end_date, result_date, result_message FROM voting_dates ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            dates_result = cursor.fetchone()
        except mysql.connector.Error as e:
            if e.errno == 1146:  # Table doesn't exist
                print("⚠️  voting_dates table doesn't exist, continuing without dates")
                dates_result = None
            else:
                raise  # Re-raise if it's a different error
        
        cursor.close()
        cnx.close()
        
        # Prepare response with voting dates
        response_data = {"candidates": candidates}
        if dates_result:
            start_date, end_date, result_date, result_message = dates_result
            if result_date:
                response_data["resultDate"] = result_date.isoformat() if hasattr(result_date, 'isoformat') else str(result_date)
            if result_message:
                response_data["resultMessage"] = result_message
        
        return response_data
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get all registered users (for admin dashboard)
@app.get("/api/users")
async def get_users(authorization: str = Header(None)):
    print("=" * 50)
    print("GET USERS ENDPOINT HIT!")
    print("=" * 50)
    print(f"Authorization: {authorization}")
    
    try:
        # Extract token from Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        # Decode token to verify it's valid
        import jwt
        from dotenv import load_dotenv
        import os
        # Load environment variables
        load_dotenv(dotenv_path="../.env")
        load_dotenv()  # Also load from current directory
        
        # Debug: Print SECRET_KEY
        secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
        print(f"[DEBUG] SECRET_KEY from env: {secret_key}")
        print(f"[DEBUG] Token: {token}")
        
        try:
            print(f"[DEBUG] Attempting to decode token with secret key: {secret_key}")
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_role = decoded.get('role')
            
            print(f"[DEBUG] Decoded token: {decoded}")
            print(f"[DEBUG] User role: {user_role}")
            
            # Check if user is admin
            if user_role != 'admin':
                raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        except jwt.ExpiredSignatureError as e:
            print(f"[DEBUG] Token expired: {e}")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(f"[DEBUG] Unexpected error during token decoding: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        
        # Query all users
        query = "SELECT firstName, lastName, emailid, voterId, has_voted FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        return users
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Serve static files (this should be after API routes)
app.mount("/static", StaticFiles(directory="../src"), name="static")
# Note: We're not mounting the HTML directory to root to avoid interfering with API routes
