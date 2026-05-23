import requests
import json

def test_otp_send():
    """Test the OTP send endpoint"""
    url = "http://127.0.0.1:8000/otp/send"  # Direct backend call
    payload = {
        "email": "test@example.com"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Testing OTP send endpoint...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_otp_send_via_frontend():
    """Test the OTP send endpoint via frontend proxy"""
    url = "http://127.0.0.1:8080/otp/send"  # Via frontend proxy
    payload = {
        "email": "test@example.com"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Testing OTP send endpoint via frontend proxy...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("OTP Fix Testing Script")
    print("=" * 30)
    
    # Test direct backend call
    backend_success = test_otp_send()
    print()
    
    # Test via frontend proxy
    frontend_success = test_otp_send_via_frontend()
    print()
    
    if backend_success and frontend_success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        if not backend_success:
            print("  - Backend test failed")
        if not frontend_success:
            print("  - Frontend proxy test failed")