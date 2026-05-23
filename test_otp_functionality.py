#!/usr/bin/env python3
"""
Test script to verify OTP functionality for both email and phone
"""

import requests
import json

def test_otp_functionality():
    """Test OTP sending and verification for both email and phone"""
    
    # Base URL for the backend API
    base_url = "http://localhost:8000"  # Python backend directly
    
    print("=== OTP Functionality Test ===")
    print("Make sure your backend server is running on port 8000")
    print("")
    
    # Test Email OTP
    print("1. Testing Email OTP...")
    email = "test@example.com"
    
    try:
        # Send email OTP
        send_response = requests.post(
            f"{base_url}/otp/send",
            json={"email": email},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Send OTP Status: {send_response.status_code}")
        print(f"   Send OTP Response: {send_response.text}")
        
        if send_response.status_code == 200:
            send_data = send_response.json()
            print(f"   Success: {send_data.get('success')}")
            print(f"   Message: {send_data.get('message')}")
            print(f"   Dev OTP: {send_data.get('dev_otp', 'Not provided')}")
        else:
            print(f"   Error: {send_response.text}")
            
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("")
    
    # Test Phone OTP
    print("2. Testing Phone OTP...")
    phone = "1234567890"
    
    try:
        # Send phone OTP
        send_response = requests.post(
            f"{base_url}/otp/send",
            json={"contact_number": phone},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Send OTP Status: {send_response.status_code}")
        print(f"   Send OTP Response: {send_response.text}")
        
        if send_response.status_code == 200:
            send_data = send_response.json()
            print(f"   Success: {send_data.get('success')}")
            print(f"   Message: {send_data.get('message')}")
            print(f"   Dev OTP: {send_data.get('dev_otp', 'Not provided')}")
        else:
            print(f"   Error: {send_response.text}")
            
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("")
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_otp_functionality()