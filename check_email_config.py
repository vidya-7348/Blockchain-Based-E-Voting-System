import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_email_config():
    print("📧 Checking Email Configuration")
    print("=" * 40)
    
    # Get configuration from environment
    email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username) or smtp_username or "noreply@example.com"
    
    print(f"EMAIL_ENABLED: {email_enabled}")
    print(f"SMTP_SERVER: {smtp_server}")
    print(f"SMTP_PORT: {smtp_port}")
    print(f"SMTP_USERNAME: {smtp_username}")
    print(f"SMTP_PASSWORD length: {len(smtp_password) if smtp_password else 0}")
    print(f"SMTP_FROM_EMAIL: {smtp_from_email}")
    
    if not email_enabled:
        print("\n❌ EMAIL_ENABLED is set to false")
        print("Set EMAIL_ENABLED=true in your .env file to enable email sending")
        return False
    
    if not smtp_username:
        print("\n❌ SMTP_USERNAME is not set")
        print("Set SMTP_USERNAME in your .env file")
        return False
    
    if not smtp_password:
        print("\n❌ SMTP_PASSWORD is not set")
        print("Set SMTP_PASSWORD in your .env file")
        return False
    
    print("\n✅ Email configuration appears to be correct")
    print("If you're still not receiving emails, check:")
    print("1. Your Gmail App Password is correct")
    print("2. 2-Factor Authentication is enabled on your Gmail account")
    print("3. Your firewall/antivirus is not blocking the connection")
    print("4. Gmail is not blocking the connection due to security settings")
    
    return True

if __name__ == "__main__":
    check_email_config()