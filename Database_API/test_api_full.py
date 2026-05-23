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
    print(f"Token: {token}")
    print(f"Token length: {len(token)}")
    
    # Test the /api/users endpoint
    users_url = "http://localhost:8000/api/users"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\nFetching users...")
    users_response = requests.get(users_url, headers=headers)
    print(f"Users status code: {users_response.status_code}")
    
    if users_response.status_code == 200:
        users_data = users_response.json()
        print(f"Users response: {json.dumps(users_data, indent=2)}")
        print("✅ Successfully fetched users!")
    else:
        print(f"❌ Error fetching users: {users_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")