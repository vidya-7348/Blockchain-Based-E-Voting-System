import requests
import json

# Test the /api/users endpoint directly on the backend
users_url = "http://localhost:8000/api/users"
headers = {
    "Authorization": "Bearer test-token"
}

print("Testing /api/users endpoint directly on backend...")
try:
    response = requests.get(users_url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test the health endpoint
health_url = "http://localhost:8000/health"
print("\nTesting /health endpoint...")
try:
    response = requests.get(health_url, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")