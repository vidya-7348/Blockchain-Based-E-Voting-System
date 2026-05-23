import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twilio_config():
    print("📱 Twilio Configuration Test")
    
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    print(f"Twilio Account SID: {twilio_account_sid}")
    print(f"Twilio Auth Token: {twilio_auth_token}")
    print(f"Twilio Phone Number: {twilio_phone_number}")
    
    if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
        print("❌ Missing Twilio credentials!")
        return False
    
    try:
        from twilio.rest import Client
        print("✅ Twilio library imported successfully")
        
        client = Client(twilio_account_sid, twilio_auth_token)
        print("✅ Twilio client created successfully")
        
        # Test with a simple phone number
        test_phone = input("Enter your phone number (with country code, e.g., +1234567890): ")
        
        print(f"🔄 Sending test SMS to {test_phone}...")
        
        message = client.messages.create(
            body="Test SMS from voting system",
            from_=twilio_phone_number,
            to=test_phone
        )
        
        print(f"✅ SMS sent successfully!")
        print(f"Message SID: {message.sid}")
        print(f"Status: {message.status}")
        return True
        
    except ImportError:
        print("❌ Twilio library not installed!")
        print("Run: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ Twilio error: {e}")
        print("\nCommon issues:")
        print("1. Wrong Twilio credentials")
        print("2. Phone number format incorrect (use +countrycode)")
        print("3. Twilio account not verified")
        print("4. Insufficient Twilio balance")
        return False

if __name__ == "__main__":
    test_twilio_config()
