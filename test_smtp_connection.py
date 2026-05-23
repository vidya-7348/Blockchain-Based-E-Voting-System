import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """
    Test SMTP connection with current configuration
    """
    print("📧 Testing SMTP Connection")
    print("=" * 40)
    
    # Get configuration from environment
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    
    print(f"SMTP_SERVER: {smtp_server}")
    print(f"SMTP_PORT: {smtp_port}")
    print(f"SMTP_USERNAME: {smtp_username}")
    print(f"SMTP_PASSWORD length: {len(smtp_password) if smtp_password else 0}")
    
    if not smtp_username or not smtp_password:
        print("\n❌ SMTP credentials not configured")
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
        
        server.quit()
        print("✅ SMTP connection test completed successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("\nCommon solutions:")
        print("1. Check that your username and password are correct")
        print("2. For Gmail, use an App Password instead of your regular password")
        print("3. Ensure 2-Factor Authentication is enabled on your Gmail account")
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
    test_smtp_connection()