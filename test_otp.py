import requests
import json

# Test the backend OTP send endpoint directly
url = "http://127.0.0.1:8000/send"
payload = {
    "email": "test@example.com"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")