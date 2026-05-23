import requests
import json

# Test the OTP endpoint directly
url = "http://localhost:8000/otp/send"
data = {"email": "test@example.com"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")