import requests
import json

# Test script to check what data is returned by the results API

def test_results_api():
    print("=== Testing Results API ===")
    
    # You'll need to replace this with a valid admin token from your system
    # For now, we'll just test if the endpoint is accessible
    url = "http://127.0.0.1:8000/api/results"
    
    try:
        # Test without authentication first
        print("Testing endpoint accessibility...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Try to parse response
        try:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_results_api()
