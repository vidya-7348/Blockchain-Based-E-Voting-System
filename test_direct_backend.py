import requests
import json

def test_direct_backend():
    """Test direct connection to backend"""
    url = "http://127.0.0.1:8000/otp/send"
    payload = {"email": "test@example.com"}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Direct backend connection successful!")
        else:
            print("❌ Direct backend connection failed!")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_direct_backend()