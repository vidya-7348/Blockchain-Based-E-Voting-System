import requests
import socket
import time

def check_port(host, port):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def test_connectivity():
    """Comprehensive connectivity test"""
    print("=== Comprehensive Connectivity Test ===")
    print("")
    
    # 1. Check if ports are open
    print("1. Checking if required ports are open...")
    backend_port_open = check_port('127.0.0.1', 8000)
    frontend_port_open = check_port('127.0.0.1', 8080)
    
    print(f"   Backend port 8000: {'✅ Open' if backend_port_open else '❌ Closed'}")
    print(f"   Frontend port 8080: {'✅ Open' if frontend_port_open else '❌ Closed'}")
    print("")
    
    if not backend_port_open:
        print("❌ BACKEND SERVER IS NOT RUNNING!")
        print("   Please start the backend server with:")
        print("   cd Database_API")
        print("   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000")
        print("")
        return False
    
    # 2. Test direct backend access
    print("2. Testing direct backend access...")
    try:
        response = requests.get('http://127.0.0.1:8000/docs', timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend documentation accessible")
        else:
            print(f"   ❌ Backend returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot access backend docs: {e}")
    
    # 3. Test OTP endpoint directly
    print("3. Testing OTP endpoint directly...")
    try:
        response = requests.post(
            'http://127.0.0.1:8000/otp/send',
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
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error testing OTP endpoint: {e}")
    
    print("")
    
    # 4. Test proxy access (if frontend is running)
    if frontend_port_open:
        print("4. Testing proxy access through frontend...")
        try:
            response = requests.post(
                'http://127.0.0.1:8080/otp/send',
                json={"email": "test@example.com"},
                headers={"Content-Type": "application/json"},
                timeout=15  # Longer timeout for proxy
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Success: {data.get('success')}")
                print(f"   Message: {data.get('message')}")
                if 'dev_otp' in data:
                    print(f"   Dev OTP: {data['dev_otp']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error testing proxy access: {e}")
    else:
        print("4. Skipping proxy test (frontend not running)")
    
    print("")
    print("=== Test Complete ===")
    return True

if __name__ == "__main__":
    test_connectivity()