import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email_otp(email: str, otp_code: str) -> bool:
    """
    Send OTP via email using Gmail SMTP with proper error handling.
    Returns True if email was sent successfully, False otherwise.
    """
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username) or smtp_username or "noreply@example.com"
        otp_ttl_minutes = int(os.getenv("EMAIL_OTP_TTL_MINUTES", "10"))
        
        print(f"[EMAIL_DEBUG] send_email_otp called with email: {email}, otp_code: {otp_code}")
        print(f"[EMAIL_DEBUG] SMTP_USERNAME: {smtp_username}")
        print(f"[EMAIL_DEBUG] SMTP_PASSWORD length: {len(smtp_password) if smtp_password else 0}")
        print(f"[EMAIL_DEBUG] SMTP_FROM_EMAIL: {smtp_from_email}")
        print(f"[EMAIL_DEBUG] SMTP_SERVER: {smtp_server}")
        print(f"[EMAIL_DEBUG] SMTP_PORT: {smtp_port}")
        
        if not smtp_username or not smtp_password:
            print("[EMAIL] SMTP credentials not configured")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_from_email
        msg['To'] = email
        msg['Subject'] = "Your OTP Code for Voting System"
        
        body = f"""Hello,

Your OTP verification code is: {otp_code}

This code will expire in {otp_ttl_minutes} minutes.

If you did not request this code, please ignore this email.

Thank you,
Voting System Team"""
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session with timeout
        print(f"[EMAIL] Connecting to SMTP server: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        print(f"[EMAIL] Connected to SMTP server")
        server.starttls()  # Enable TLS encryption
        print("[EMAIL] TLS encryption enabled")
        print(f"[EMAIL] Logging in to SMTP server")
        print(f"[EMAIL] Using username: {smtp_username}")
        # Mask password for security in logs
        masked_password = '*' * len(smtp_password) if smtp_password else 'None'
        print(f"[EMAIL] Using password: {masked_password}")
        server.login(smtp_username, smtp_password)
        print("[EMAIL] Successfully logged in to SMTP server")
        
        # Send email
        print(f"[EMAIL] Sending email to {email}")
        text = msg.as_string()
        server.sendmail(smtp_from_email, email, text)
        print(f"[EMAIL] Email sent command executed")
        server.quit()
        print(f"[EMAIL] SMTP connection closed")
        
        print(f"✅ Email OTP sent successfully to {email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print(f"❌ This usually means the username or password is incorrect.")
        print(f"❌ Please check that your app password is correct and hasn't been revoked.")
        print(f"❌ Make sure 2-factor authentication is enabled on your Gmail account.")
        print(f"❌ Make sure 'Less secure app access' is turned OFF in your Google account settings.")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ SMTP Recipients Refused: {e}")
        print(f"❌ This usually means the recipient email address is invalid or blocked.")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SMTP Server Disconnected: {e}")
        print(f"❌ This usually means the connection to the SMTP server was lost.")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP Connection Error: {e}")
        print(f"❌ This usually means the SMTP server address or port is incorrect.")
        return False
    except smtplib.SMTPHeloError as e:
        print(f"❌ SMTP HELO Error: {e}")
        print(f"❌ This usually means the server didn't reply properly to the HELO greeting.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        print(f"❌ This is a general SMTP error.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_send_otp_email():
    """
    Test sending OTP email with current configuration
    """
    print("📧 Testing OTP Email Sending")
    print("=" * 40)
    
    # Test with a real email address
    test_email = "test@example.com"
    otp_code = "123456"
    
    print(f"Sending OTP {otp_code} to {test_email}")
    result = send_email_otp(test_email, otp_code)
    print(f"Result: {result}")
    
    if result:
        print("✅ OTP email sending test completed successfully!")
    else:
        print("❌ OTP email sending test failed!")

if __name__ == "__main__":
    test_send_otp_email()