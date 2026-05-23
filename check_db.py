import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

try:
    # Connect to database
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    
    cursor = cnx.cursor(dictionary=True)
    
    # Check total users
    cursor.execute("SELECT COUNT(*) as count FROM users")
    result = cursor.fetchone()
    if result:
        # Access the first column (count)
        count = list(result.values())[0] if isinstance(result, dict) else result[0]
        print(f"Total users in database: {count}")
    
    # Check admin users
    cursor.execute("SELECT voterId, emailid, role FROM users WHERE role = 'admin'")
    admins = cursor.fetchall()
    print("Admin users in database:")
    for admin in admins:
        # Access columns by index or key depending on the type
        if isinstance(admin, dict):
            voter_id = admin.get('voterId', 'N/A')
            email = admin.get('emailid', 'N/A')
            role = admin.get('role', 'N/A')
        else:
            voter_id = admin[0]
            email = admin[1]
            role = admin[2]
        print(f"  - ID: {voter_id}, Email: {email}, Role: {role}")
    
    # Check if there's at least one admin user
    if len(admins) == 0:
        print("WARNING: No admin users found in the database!")
        print("You need to create an admin user to access the admin dashboard.")
    
    cnx.close()
    
except Exception as e:
    print(f"Error connecting to database: {e}")