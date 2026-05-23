import os
import mysql.connector
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional

# Helper function to get database connection
def get_db_connection():
    from dotenv import load_dotenv
    import os
    
    # Load environment variables
    load_dotenv(dotenv_path="../.env")
    load_dotenv()  # Also load from current directory
    
    # Connect to database
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    return cnx

# Safe registration function that works with your current table structure
def safe_register(payload):
    # Registration endpoint
    
    try:
        # Validate passwords match
        if payload.confirmPassword and payload.password != payload.confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        # Connect to database
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Check if user already exists by email
        query = "SELECT emailid FROM users WHERE emailid = %s"
        cursor.execute(query, (payload.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            cnx.close()
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Check if voterId already exists
        query = "SELECT voterId FROM users WHERE voterId = %s"
        cursor.execute(query, (payload.voterId,))
        existing_voter = cursor.fetchone()
        
        if existing_voter:
            cursor.close()
            cnx.close()
            raise HTTPException(status_code=400, detail="Voter ID already registered")
        
        # Check if Aadhaar already exists
        query = "SELECT aadhar FROM users WHERE aadhar = %s"
        cursor.execute(query, (payload.aadhar,))
        existing_aadhar = cursor.fetchone()
        
        if existing_aadhar:
            cursor.close()
            cnx.close()
            raise HTTPException(status_code=400, detail="Aadhaar number already registered")
        
        # Insert new user with all required fields including has_voted
        query = """INSERT INTO users 
                   (firstName, middleName, lastName, emailid, password, voterId, contactNumber, aadhar, dob, age, gender, address, role, has_voted) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Ensure all values are provided (your table has NOT NULL constraints)
        values = (
            payload.firstName,
            payload.middleName or '',
            payload.lastName,
            payload.email,
            payload.password,  # In production, hash this with bcrypt
            payload.voterId,
            payload.contactNumber,
            payload.aadhar or '000000000000',  # Cannot be NULL
            payload.dob or '2000-01-01',       # Cannot be NULL
            payload.age or 18,                 # Cannot be NULL
            payload.gender or 'Other',         # Cannot be NULL
            payload.address or '',             # Cannot be NULL
            'user',  # role defaults to 'user'
            0        # has_voted defaults to 0 (FALSE)
        )
        
        cursor.execute(query, values)
        cnx.commit()
        
        cursor.close()
        cnx.close()
        
        return {
            "success": True,
            "message": "Registration successful"
        }
        
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Registration request model
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