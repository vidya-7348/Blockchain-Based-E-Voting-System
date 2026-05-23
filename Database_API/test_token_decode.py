import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the SECRET_KEY
secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
print(f"SECRET_KEY: {secret_key}")

# The token from the login endpoint
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InZhaXNobmF2aXB1amFyaTQ0NDRAZ21haWwuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY0Mzk4NTc4LjQ1NzYxOTd9.CHpovbIcT-Mys7byN5R6N4Y4sYha3"

print(f"Token: {token}")

# Try to decode the token
try:
    print(f"Attempting to decode token with secret key: {secret_key}")
    decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    print(f"Decoded payload: {decoded_payload}")
    print("✅ Token decoding works correctly!")
except Exception as e:
    print(f"❌ Error decoding token: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()