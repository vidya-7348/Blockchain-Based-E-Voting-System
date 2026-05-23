import requests
import json
from datetime import datetime

# Test script to check user results API and date logic

def test_user_results():
    print("=== Testing User Results API ===")
    
    # Print current date and time
    current_time = datetime.now()
    print(f"Current date/time: {current_time}")
    
    # You'll need to replace this with a valid user token from your system
    # For now, we'll just test if the endpoint is accessible
    url = "http://127.0.0.1:8000/api/user/results"
    
    try:
        # Test without authentication first
        print("Testing endpoint accessibility...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Try to parse response
        try:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2, default=str)}")
            
            # Check if we have voting dates
            if "resultDate" in data:
                result_date = datetime.fromisoformat(data["resultDate"].replace('Z', '+00:00'))
                print(f"Result date from API: {result_date}")
                print(f"Current date: {current_time}")
                print(f"Has result date passed? {current_time >= result_date}")
            else:
                print("No result date in response")
                
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_user_results()