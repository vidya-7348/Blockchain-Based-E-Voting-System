import requests
import json

# Test script to verify candidate addition functionality

def test_add_candidate():
    url = "http://localhost:8000/candidates"
    
    # Test data
    data = {
        "name": "Test Candidate",
        "party": "Test Party"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Try to parse response as JSON
        try:
            response_data = response.json()
            print(f"Response JSON: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_add_candidate()