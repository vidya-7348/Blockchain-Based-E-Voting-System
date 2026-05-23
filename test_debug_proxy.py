import requests
import json

# Test the /api/users endpoint through the debug proxy
users_url = "http://localhost:8081/api/users"
headers = {
    "Authorization": "Bearer test-token"
}

print("Testing /api/users endpoint through debug proxy...")
try:
    response = requests.get(users_url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")