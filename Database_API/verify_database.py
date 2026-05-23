import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path="../.env")

print("=== DATABASE CONNECTION TEST ===")

try:
    # Test database connection
    print("Connecting to database...")
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    print("✅ Database connection successful")
    
    cursor = cnx.cursor(dictionary=True)
    
    # Test users query
    print("\n=== TESTING USERS QUERY ===")
    query = "SELECT firstName, lastName, emailid, voterId, has_voted FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users:")
    for i, user in enumerate(users, 1):
        print(f"  {i}. {user['firstName']} {user['lastName']} ({user['emailid']}) - Voter ID: {user['voterId']} - Voted: {user['has_voted']}")
    
    # Test candidates query
    print("\n=== TESTING CANDIDATES QUERY ===")
    query = "SELECT id, name, party, COALESCE(vote_count, 0) as vote_count FROM candidates ORDER BY vote_count DESC"
    cursor.execute(query)
    candidates = cursor.fetchall()
    
    print(f"Found {len(candidates)} candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"  {i}. {candidate['name']} ({candidate['party']}) - Votes: {candidate['vote_count']}")
    
    cursor.close()
    cnx.close()
    
    print("\n✅ All database queries successful")
    
except mysql.connector.Error as e:
    print(f"❌ Database error: {e}")
except KeyError as e:
    print(f"❌ Missing environment variable: {e}")
    print("Available environment variables:")
    for key in ['MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_DB']:
        value = os.environ.get(key, 'NOT SET')
        print(f"  {key}: {value}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()