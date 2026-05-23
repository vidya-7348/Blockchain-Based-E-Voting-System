import requests
import json

# Test the /api/users endpoint through the isolated server
users_url = "http://localhost:8084/api/users"
headers = {
    "Authorization": "Bearer test-token"
}

print("Testing /api/users endpoint through isolated server...")
try:
    response = requests.get(users_url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")