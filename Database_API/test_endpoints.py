import requests
import json

# Test the /api/users endpoint
users_url = "http://localhost:8000/api/users"
headers = {
    "Authorization": "Bearer test-token"
}

print("Testing /api/users endpoint...")
try:
    response = requests.get(users_url, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting /api/results endpoint...")
# Test the /api/results endpoint
results_url = "http://localhost:8000/api/results"
try:
    response = requests.get(results_url, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")