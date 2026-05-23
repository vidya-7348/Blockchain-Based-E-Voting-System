import os
import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def test_jwt_decoding():
    print("=== JWT Decoding Test ===")
    
    # Get secret key
    secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
    print(f"Secret key length: {len(secret_key)} characters")
    print(f"Secret key (first 10 chars): {secret_key[:10]}...")
    
    # Create a test token
    test_payload = {
        'email': 'test@example.com',
        'role': 'user',
        'exp': 9999999999
    }
    
    print(f"Test payload: {test_payload}")
    
    try:
        # Encode token
        test_token = jwt.encode(test_payload, secret_key, algorithm='HS256')
        print(f"✅ Token encoded successfully")
        print(f"Token (first 50 chars): {test_token[:50]}...")
        
        # Decode token
        decoded = jwt.decode(test_token, secret_key, algorithms=['HS256'])
        print(f"✅ Token decoded successfully: {decoded}")
        
    except Exception as e:
        print(f"❌ JWT handling failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jwt_decoding()