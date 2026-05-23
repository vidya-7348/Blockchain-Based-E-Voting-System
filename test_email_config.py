import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / "Database_API" / ".env")

# Get email configuration
smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.environ.get("SMTP_PORT", "587"))
email_username = os.environ.get("SMTP_USERNAME")
email_password = os.environ.get("SMTP_PASSWORD")
email_enabled = all([email_username, email_password])

print(f"SMTP Server: {smtp_server}")
print(f"SMTP Port: {smtp_port}")
print(f"Email Username: {email_username}")
print(f"Email Password configured: {'Yes' if email_password else 'No'}")
print(f"Email Enabled: {email_enabled}")

if email_enabled:
    try:
        print("Testing email configuration...")
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = email_username  # Send to self for testing
        msg['Subject'] = "Test Email Configuration"
        
        body = "This is a test email to verify the email configuration."
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"Connecting to SMTP server {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print(f"Logging in with username: {email_username}")
        server.login(email_username, email_password)
        text = msg.as_string()
        server.sendmail(email_username, email_username, text)
        server.quit()
        print("✅ Email configuration test successful!")
    except Exception as e:
        print(f"❌ Email configuration test failed: {e}")
else:
    print("Email configuration is incomplete. Please check your .env file.")