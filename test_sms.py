import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sms_config():
    print("📱 SMS Configuration Test")
    
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    print(f"Twilio Account SID: {'✅ Set' if twilio_account_sid else '❌ Not Set'}")
    print(f"Twilio Auth Token: {'✅ Set' if twilio_auth_token else '❌ Not Set'}")
    print(f"Twilio Phone Number: {twilio_phone_number or '❌ Not Set'}")
    
    if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
        print("\n❌ Twilio credentials not configured!")
        print("Please add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to your .env file")
        print("\nTo get Twilio credentials:")
        print("1. Sign up at https://twilio.com")
        print("2. Get Account SID and Auth Token from Console")
        print("3. Buy a phone number from Twilio")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(twilio_account_sid, twilio_auth_token)
        
        test_phone = input("\nEnter your phone number (with country code, e.g., +1234567890): ")
        
        print(f"🔄 Sending test SMS to {test_phone}...")
        
        message = client.messages.create(
            body="This is a test SMS from your voting system. If you receive this, SMS is working!",
            from_=twilio_phone_number,
            to=test_phone
        )
        
        print(f"✅ Test SMS sent successfully!")
        print(f"Message SID: {message.sid}")
        print("Check your phone for the test message.")
        return True
        
    except ImportError:
        print("❌ Twilio library not installed!")
        print("Run: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ Failed to send test SMS: {e}")
        print("\nCommon issues:")
        print("1. Wrong Twilio credentials")
        print("2. Phone number format incorrect")
        print("3. Twilio account not verified")
        return False

if __name__ == "__main__":
    test_sms_config()
