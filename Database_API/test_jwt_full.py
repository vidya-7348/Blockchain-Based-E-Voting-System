import jwt
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the SECRET_KEY
secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
print(f"SECRET_KEY: {secret_key}")

# Create a test token (same as login endpoint)
test_payload = {
    'email': 'vaishnavipujari4444@gmail.com',
    'role': 'admin',
    'exp': time.time() + 3600  # 1 hour expiration
}

print(f"Test payload: {test_payload}")

# Encode the token (same as login endpoint)
encoded_token = jwt.encode(test_payload, secret_key, algorithm='HS256')
print(f"Encoded token: {encoded_token}")

# Decode the token (same as get_users endpoint)
try:
    print(f"Attempting to decode token with secret key: {secret_key}")
    decoded_payload = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
    print(f"Decoded payload: {decoded_payload}")
    print("✅ Token encoding and decoding works correctly!")
except Exception as e:
    print(f"❌ Error decoding token: {e}")
    print(f"Error type: {type(e)}")