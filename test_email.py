import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_config():
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    email_username = os.environ.get("SMTP_USERNAME")
    email_password = os.environ.get("SMTP_PASSWORD")
    
    print("📧 Email Configuration Test")
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Email Username: {email_username}")
    print(f"Email Password: {'✅ Set' if email_password else '❌ Not Set'}")
    
    if not email_username or not email_password:
        print("\n❌ Email credentials not configured!")
        print("Please add EMAIL_USERNAME and EMAIL_PASSWORD to your .env file")
        return False
    
    # Test email sending
    test_email = input("\nEnter your email address to test: ")
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = test_email
        msg['Subject'] = "Voting System - Email Test"
        
        body = """
        This is a test email from your voting system.
        
        If you receive this email, your email configuration is working correctly!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"\n🔄 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print(f"🔄 Logging in with {email_username}...")
        server.login(email_username, email_password)
        
        print(f"🔄 Sending test email to {test_email}...")
        text = msg.as_string()
        server.sendmail(email_username, test_email, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("Check your email inbox for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        print("\nCommon issues:")
        print("1. Wrong email/password")
        print("2. Need to use App Password for Gmail")
        print("3. 2-Factor Authentication not enabled")
        print("4. SMTP settings incorrect")
        return False

if __name__ == "__main__":
    test_email_config()
