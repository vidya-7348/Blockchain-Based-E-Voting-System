import jwt
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the SECRET_KEY
secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
print(f"SECRET_KEY: {secret_key}")

# Create a test token
test_payload = {
    'email': 'test@example.com',
    'role': 'admin',
    'exp': time.time() + 3600  # 1 hour expiration
}

# Encode the token
encoded_token = jwt.encode(test_payload, secret_key, algorithm='HS256')
print(f"Encoded token: {encoded_token}")

# Decode the token
try:
    decoded_payload = jwt.decode(encoded_token, secret_key, algorithms=['HS256'])
    print(f"Decoded payload: {decoded_payload}")
    print("✅ Token encoding and decoding works correctly!")
except Exception as e:
    print(f"❌ Error decoding token: {e}")