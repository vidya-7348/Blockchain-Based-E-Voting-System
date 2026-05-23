#!/usr/bin/env python3
"""
Test script to verify Gmail OTP functionality
"""

import os
import sys
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from both .env files
load_dotenv()
load_dotenv(dotenv_path="Database_API/.env")

def test_gmail_otp():
    """Test Gmail OTP sending functionality"""
    
    # Get email configuration
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    email_username = os.environ.get("SMTP_USERNAME") or os.environ.get("EMAIL_USERNAME") or ""
    email_password = os.environ.get("SMTP_PASSWORD") or os.environ.get("EMAIL_PASSWORD") or ""
    from_email = os.environ.get("SMTP_FROM_EMAIL", email_username) or email_username or "noreply@example.com"
    
    print("=== Gmail OTP Configuration Test ===")
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Email Username: {email_username}")
    print(f"From Email: {from_email}")
    print(f"Password Set: {'Yes' if email_password else 'No'}")
    print("")
    
    # Validate configuration
    if not email_username or not email_password:
        print("❌ ERROR: Email credentials not configured!")
        print("Please ensure SMTP_USERNAME and SMTP_PASSWORD are set in your .env file")
        return False
    
    # Get test email
    test_email = input("Enter your email address to test: ")
    if not test_email:
        print("❌ ERROR: Test email address required")
        return False
    
    # Generate test OTP
    otp_code = "123456"
    print(f"Generated test OTP: {otp_code}")
    print("")
    
    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        print("Connected successfully!")
        
        print("Enabling TLS encryption...")
        context = ssl.create_default_context()
        server.starttls(context=context)
        print("TLS enabled!")
        
        print("Logging in...")
        server.login(email_username, email_password)
        print("Login successful!")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = test_email
        msg['Subject'] = "Test OTP Code for Voting System"
        
        body = f"""Hello,

This is a test OTP email from your Voting System.

Your test OTP code is: {otp_code}

If you received this email, your Gmail SMTP configuration is working correctly!

Thank you,
Voting System Team"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        print("Sending email...")
        text = msg.as_string()
        server.sendmail(from_email, test_email, text)
        print("Email sent successfully!")
        
        server.quit()
        print("Connection closed.")
        
        print("\n✅ SUCCESS: Gmail OTP configuration is working!")
        print(f"Check your email at {test_email} for the test OTP.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ SMTP AUTHENTICATION ERROR: {e}")
        print("\nPossible causes:")
        print("1. Incorrect email username or password")
        print("2. For Gmail, you MUST use an App Password, not your regular password")
        print("3. 2-Factor Authentication must be enabled on your Gmail account")
        print("4. Go to https://myaccount.google.com/apppasswords to generate an App Password")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"\n❌ RECIPIENT REFUSED ERROR: {e}")
        print("The recipient email address may be invalid or blocked")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"\n❌ SERVER DISCONNECTED ERROR: {e}")
        print("The connection to the SMTP server was lost")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("Could not connect to the SMTP server")
        print("Check your SMTP server address and port")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Gmail OTP Configuration Tester")
    print("=" * 40)
    print("")
    
    success = test_gmail_otp()
    
    print("\n" + "=" * 40)
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed. Please check the error messages above.")