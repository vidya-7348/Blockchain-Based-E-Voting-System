import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_test_email():
    """
    Send a test email with current configuration
    """
    print("📧 Sending Test Email")
    print("=" * 40)
    
    # Get configuration from environment
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username) or smtp_username or "noreply@example.com"
    
    # Get test email address
    test_email = input("Enter your email address to test: ")
    if not test_email:
        print("❌ No email address provided")
        return False
    
    try:
        print(f"\n🔄 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        print("✅ Connected to SMTP server")
        
        print("🔄 Starting TLS encryption...")
        server.starttls()
        print("✅ TLS encryption enabled")
        
        print(f"🔄 Logging in as {smtp_username}...")
        server.login(smtp_username, smtp_password)
        print("✅ Successfully logged in to SMTP server")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = smtp_from_email
        msg['To'] = test_email
        msg['Subject'] = "Voting System - Email Test"
        
        body = """
        This is a test email from your voting system.
        
        If you receive this email, your email configuration is working correctly!
        
        OTP Test Code: 123456
        
        Thank you,
        Voting System Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"🔄 Sending test email to {test_email}...")
        text = msg.as_string()
        server.sendmail(smtp_from_email, test_email, text)
        print("✅ Test email sent successfully!")
        
        server.quit()
        print("✅ SMTP connection closed")
        print("Check your email inbox for the test message.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("\nCommon solutions:")
        print("1. Check that your username and password are correct")
        print("2. For Gmail, use an App Password instead of your regular password")
        print("3. Ensure 2-Factor Authentication is enabled on your Gmail account")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ SMTP Recipients Refused: {e}")
        print("Check that the recipient email address is valid")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SMTP Server Disconnected: {e}")
        print("Check your internet connection and SMTP server settings")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP Connection Error: {e}")
        print("Check your SMTP server address and port")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    send_test_email()