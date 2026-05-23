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
    print(f"Login successful")
    
    token = login_data.get("token")
    
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
        print(f"Number of users returned: {len(users_data)}")
        print(f"Users data: {json.dumps(users_data, indent=2)}")
        
        # Check if it's a list or dict
        if isinstance(users_data, list):
            print("✅ Response is a list (correct format)")
            if len(users_data) > 0:
                print("✅ Users list is not empty")
                for i, user in enumerate(users_data):
                    print(f"  User {i+1}: {user.get('firstName', '')} {user.get('lastName', '')} - {user.get('emailid', '')}")
            else:
                print("❌ Users list is empty")
        else:
            print("❌ Response is not a list")
    else:
        print(f"❌ Error fetching users: {users_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")