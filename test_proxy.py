import requests
import json

# Test the /api/users endpoint through the frontend proxy
users_url = "http://localhost:8080/api/users"
headers = {
    "Authorization": "Bearer test-token"
}

print("Testing /api/users endpoint through frontend proxy...")
try:
    response = requests.get(users_url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test a simple frontend page to make sure frontend is running
frontend_url = "http://localhost:8080/"
print("\nTesting frontend root...")
try:
    response = requests.get(frontend_url, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Content length: {len(response.text)}")
except Exception as e:
    print(f"Error: {e}")