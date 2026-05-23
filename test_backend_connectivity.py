#!/usr/bin/env python3
"""
Test script to verify backend connectivity
"""

import requests
import time

def test_backend_connectivity():
    """Test if the backend is accessible"""
    
    # Test direct connection to backend
    backend_url = "http://127.0.0.1:8000"
    
    print("=== Backend Connectivity Test ===")
    print(f"Testing connection to backend at {backend_url}")
    print("")
    
    try:
        # Test if backend is running
        response = requests.get(f"{backend_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible!")
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        else:
            print(f"❌ Backend returned unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("   Make sure the Python backend is running:")
        print("   cd Database_API")
        print("   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection to backend timed out!")
        print("   The backend might be running but not responding in time")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("")
    
    # Test OTP endpoint
    try:
        print("Testing OTP endpoint...")
        otp_response = requests.post(
            f"{backend_url}/otp/send",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   OTP Send Status: {otp_response.status_code}")
        if otp_response.status_code == 200:
            data = otp_response.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            if 'dev_otp' in data:
                print(f"   Dev OTP: {data['dev_otp']}")
        else:
            print(f"   Error Response: {otp_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing OTP endpoint: {e}")
    
    print("")
    print("=== Test Complete ===")
    return True

if __name__ == "__main__":
    test_backend_connectivity()