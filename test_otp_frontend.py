import requests
import json

def test_otp_frontend():
    """Test OTP functionality through frontend proxy"""
    
    url = "http://localhost:8080/otp/send"
    payload = {"email": "test@example.com"}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("Success:", data.get("success"))
            print("Message:", data.get("message"))
            if "dev_otp" in data:
                print("Dev OTP:", data["dev_otp"])
        else:
            print("Error occurred")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_otp_frontend()