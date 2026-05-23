import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Connect to database
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    cursor = cnx.cursor(dictionary=True)
    
    # Query all users with passwords
    query = "SELECT firstName, lastName, emailid, password, voterId, has_voted, role FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users in the database:")
    for user in users:
        print(f"  - {user['firstName']} {user['lastName']} ({user['emailid']}) - Role: {user['role']} - Password: {user['password']} - Voter ID: {user['voterId']} - Voted: {user['has_voted']}")
    
    cursor.close()
    cnx.close()
    
except mysql.connector.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")