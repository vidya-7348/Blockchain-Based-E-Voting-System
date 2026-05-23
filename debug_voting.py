import os
import sys
import traceback
from dotenv import load_dotenv

# Add the Database_API directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database_API'))

def debug_voting():
    print("=== Voting Debug Script ===")
    
    # Load environment variables
    load_dotenv(dotenv_path="Database_API/.env")
    print("Environment variables loaded")
    
    # Check required environment variables
    required_vars = ['MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_DB', 'SECRET_KEY']
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            if var == 'MYSQL_PASSWORD' or var == 'SECRET_KEY':
                print(f"{var}: {'*' * len(value)}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: NOT SET")
    
    # Test database connection
    print("\n--- Testing Database Connection ---")
    try:
        from Database_API.main import get_db_connection
        cnx = get_db_connection()
        print("✅ Database connection successful")
        
        # Test querying users table
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        print(f"Users table has {result['count']} records")
        
        # Test querying candidates table
        cursor.execute("SELECT COUNT(*) as count FROM candidates")
        result = cursor.fetchone()
        print(f"Candidates table has {result['count']} records")
        
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        traceback.print_exc()
    
    # Test importing voting_api
    print("\n--- Testing Voting API Import ---")
    try:
        from Database_API.voting_api import vote
        print("✅ Voting API imported successfully")
    except Exception as e:
        print(f"❌ Voting API import failed: {e}")
        traceback.print_exc()
    
    # Test JWT token decoding
    print("\n--- Testing JWT Token Decoding ---")
    try:
        import jwt
        secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
        # Create a test token
        test_token = jwt.encode({
            'email': 'test@example.com',
            'role': 'user',
            'exp': 9999999999
        }, secret_key, algorithm='HS256')
        print(f"Test token created: {test_token[:20]}...")
        
        # Decode the token
        decoded = jwt.decode(test_token, secret_key, algorithms=['HS256'])
        print(f"✅ Token decoded successfully: {decoded}")
    except Exception as e:
        print(f"❌ JWT token handling failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_voting()