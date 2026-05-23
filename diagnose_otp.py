#!/usr/bin/env python3
"""
Diagnostic script to test OTP functionality directly
"""

import os
import sys
from pathlib import Path

# Add the Database_API directory to the path
project_root = Path(__file__).parent
database_api_path = project_root / "Database_API"
sys.path.insert(0, str(database_api_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=database_api_path / ".env")

# Import required modules
import random
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get email configuration
smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.environ.get("SMTP_PORT", "587"))
email_username = os.environ.get("SMTP_USERNAME")
email_password = os.environ.get("SMTP_PASSWORD")
email_enabled = all([email_username, email_password])

print("=== OTP System Diagnostic ===")
print(f"Project Root: {project_root}")
print(f"Database API Path: {database_api_path}")
print(f"SMTP Server: {smtp_server}:{smtp_port}")
print(f"Email Username: {email_username}")
print(f"Email Password Set: {'Yes' if email_password else 'No'}")
print(f"Email Enabled: {email_enabled}")
print("")

# Test email sending function
def test_email_sending():
    """Test email sending functionality"""
    email = "test@example.com"
    otp_code = f"{random.randint(0, 999999):06d}"
    
    print(f"Testing email sending to: {email}")
    print(f"Generated OTP: {otp_code}")
    print("")
    
    if not email_enabled:
        print("[INFO] Email not enabled - this is expected in development mode")
        print("[INFO] In development mode, OTP would be displayed in console")
        return True
    
    try:
        print("Attempting to connect to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("Starting TLS...")
        server.starttls()
        print("Logging in...")
        server.login(email_username, email_password)
        
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = email
        msg['Subject'] = "Voting System - Email Verification Code"
        
        body = f"""
        Your email verification code is: {otp_code}
        
        This code will expire in 5 minutes.
        
        If you did not request this code, please ignore this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(email_username, email, text)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("This usually means:")
        print("  1. Incorrect email username or password")
        print("  2. For Gmail, you may need an App Password instead of your regular password")
        print("  3. Gmail security settings may be blocking the login")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ SMTP Recipients Refused: {e}")
        print("This usually means the recipient email address is invalid")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_email_sending()
    print("\n=== Diagnostic Complete ===")