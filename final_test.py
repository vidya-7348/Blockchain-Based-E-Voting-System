import requests
import time

def test_system():
    """Final test to verify the system is working correctly"""
    
    print("=== Final System Test ===")
    print("Testing if both frontend and backend are working together")
    print("")
    
    # Test 1: Check if frontend is running
    print("1. Testing frontend server...")
    try:
        response = requests.get('http://localhost:8080', timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend server is running")
        else:
            print(f"   ❌ Frontend server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to frontend: {e}")
        return False
    
    # Test 2: Check if backend is running
    print("2. Testing backend server...")
    try:
        response = requests.get('http://127.0.0.1:8000/docs', timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend server is running")
        else:
            print(f"   ❌ Backend server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return False
    
    # Test 3: Test OTP functionality through proxy
    print("3. Testing OTP functionality through frontend proxy...")
    try:
        response = requests.post(
            'http://localhost:8080/otp/send',
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            if 'dev_otp' in data:
                print(f"   Dev OTP: {data['dev_otp']}")
            print("   ✅ OTP functionality is working!")
        else:
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error testing OTP functionality: {e}")
        return False
    
    print("")
    print("🎉 ALL TESTS PASSED! Your system is working correctly.")
    print("")
    print("You can now access the admin login page at:")
    print("http://localhost:8080/admin_login.html")
    print("")
    print("When you send an OTP, you should see the code in the browser console")
    print("and in alerts (if OTP_DEBUG=true in your .env file)")
    
    return True

if __name__ == "__main__":
    test_system()