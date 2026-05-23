import requests
import time

def test_connectivity():
    """Test connectivity to both frontend and backend servers"""
    
    print("Testing server connectivity...")
    print("=" * 50)
    
    # Test backend server
    print("1. Testing backend server (localhost:8000)...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Backend server is running")
        else:
            print("   ❌ Backend server returned unexpected status")
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend server - make sure it's running")
    except Exception as e:
        print(f"   ❌ Error connecting to backend: {e}")
    
    print()
    
    # Test frontend server
    print("2. Testing frontend server (localhost:8080)...")
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend server is running")
        else:
            print("   ❌ Frontend server returned unexpected status")
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to frontend server - make sure it's running")
    except Exception as e:
        print(f"   ❌ Error connecting to frontend: {e}")
    
    print()
    
    # Test OTP endpoint directly
    print("3. Testing OTP endpoint directly...")
    try:
        response = requests.post(
            "http://localhost:8000/otp/send",
            json={"email": "test@example.com"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ OTP endpoint is working")
        else:
            print("   ❌ OTP endpoint returned unexpected status")
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to OTP endpoint")
    except Exception as e:
        print(f"   ❌ Error testing OTP endpoint: {e}")
    
    print()
    print("=" * 50)
    print("Connectivity test completed")

if __name__ == "__main__":
    test_connectivity()