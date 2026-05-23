import requests
import json

# Login to get a token
login_url = "http://localhost:8000/login"
login_params = {
    "email": "vaishnavipujari4444@gmail.com",
    "password": "Admin@123"
}

print("Logging in...")
login_response = requests.get(login_url, params=login_params)
print(f"Login status code: {login_response.status_code}")

if login_response.status_code == 200:
    login_data = login_response.json()
    print(f"Login response: {json.dumps(login_data, indent=2)}")
    
    token = login_data.get("token")
    print(f"Token length: {len(token)}")
    
    # Test the /api/results endpoint
    results_url = "http://localhost:8000/api/results"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\nFetching results...")
    results_response = requests.get(results_url, headers=headers)
    print(f"Results status code: {results_response.status_code}")
    
    if results_response.status_code == 200:
        results_data = results_response.json()
        print(f"Results response: {json.dumps(results_data, indent=2)}")
        print("✅ Successfully fetched results!")
    else:
        print(f"❌ Error fetching results: {results_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")