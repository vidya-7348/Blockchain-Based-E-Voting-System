import requests
import json

# Test script to verify voting endpoint functionality

def test_voting_endpoint():
    # First, let's login to get a token
    login_url = "http://localhost:8000/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        # Try to login
        login_response = requests.get(login_url, params=login_data)
        print(f"Login Status Code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print(f"Login Response: {json.dumps(login_result, indent=2)}")
            
            # Extract token
            token = login_result.get("token")
            if token:
                # Test voting endpoint
                vote_url = "http://localhost:8000/vote"
                vote_data = {
                    "candidateId": 1
                }
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                vote_response = requests.post(vote_url, json=vote_data, headers=headers)
                print(f"Vote Status Code: {vote_response.status_code}")
                
                # Try to parse response as JSON
                try:
                    vote_result = vote_response.json()
                    print(f"Vote Response JSON: {json.dumps(vote_result, indent=2)}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON: {e}")
                    print(f"Response Text: {vote_response.text}")
            else:
                print("No token received from login")
        else:
            print(f"Login failed with status {login_response.status_code}")
            print(f"Response Text: {login_response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_voting_endpoint()