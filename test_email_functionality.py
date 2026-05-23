import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_functionality():
    """
    Test the email functionality with current .env configuration
    """
    print("📧 Testing Email Configuration")
    print("=" * 40)
    
    # Get configuration from environment
    email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username) or smtp_username or "noreply@example.com"
    
    print(f"Email Enabled: {email_enabled}")
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"SMTP Username: {smtp_username}")
    print(f"SMTP Password Set: {'✅ Yes' if smtp_password else '❌ No'}")
    print(f"From Email: {smtp_from_email}")
    
    if not email_enabled:
        print("\n⚠️  Email is disabled in configuration")
        print("To test email functionality, set EMAIL_ENABLED=true in your .env file")
        return False
    
    if not smtp_username or not smtp_password:
        print("\n❌ SMTP credentials not configured properly")
        print("Please set SMTP_USERNAME and SMTP_PASSWORD in your .env file")
        return False
    
    # Get test email address
    test_email = input("\nEnter your email address to test: ")
    if not test_email:
        print("❌ No email address provided")
        return False
    
    try:
        print(f"\n🔄 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.set_debuglevel(1)  # Enable debug output
        print("🔄 Starting TLS encryption...")
        server.starttls()
        
        print(f"🔄 Logging in as {smtp_username}...")
        server.login(smtp_username, smtp_password)
        
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
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("Check your email inbox for the test message.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("\nCommon solutions:")
        print("1. Check that your username and password are correct")
        print("2. For Gmail, use an App Password instead of your regular password")
        print("3. Ensure 2-Factor Authentication is enabled on your account")
        print("4. Check that 'Less secure app access' is turned OFF")
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
    test_email_functionality()