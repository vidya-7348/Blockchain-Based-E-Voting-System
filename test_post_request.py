import requests
import json

def test_otp_post():
    """Test OTP POST request directly to frontend proxy"""
    url = "http://127.0.0.1:8081/otp/send"
    payload = {
        "email": "test@example.com"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Testing OTP POST request...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ POST request successful!")
            return True
        else:
            print("❌ POST request failed!")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_otp_get():
    """Test OTP GET request to see if it fails with 405"""
    url = "http://127.0.0.1:8081/otp/send"
    
    try:
        print("\nTesting OTP GET request...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 405:
            print("✅ GET request correctly returns 405 Method Not Allowed")
            return True
        else:
            print("❌ GET request returned unexpected status")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("OTP Request Testing")
    print("=" * 30)
    
    post_success = test_otp_post()
    get_success = test_otp_get()
    
    print("\n" + "=" * 30)
    if post_success and get_success:
        print("✅ All tests completed as expected!")
    else:
        print("❌ Some tests failed!")