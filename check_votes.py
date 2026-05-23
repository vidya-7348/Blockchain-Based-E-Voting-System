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
        database=os.environ['MYSQL_DB']
    )
    cursor = cnx.cursor()
    
    # Query users and their voting status
    cursor.execute('SELECT firstName, lastName, emailid, has_voted FROM users')
    results = cursor.fetchall()
    
    print('Users and their voting status:')
    for row in results:
        print(f"Name: {row[0]} {row[1]}, Email: {row[2]}, Has Voted: {row[3]}")
    
    # Query candidates with vote counts
    cursor.execute('SELECT name, party, vote_count FROM candidates')
    candidates = cursor.fetchall()
    
    print('\nCandidates and their vote counts:')
    for row in candidates:
        print(f"Name: {row[0]}, Party: {row[1]}, Votes: {row[2]}")
    
    cursor.close()
    cnx.close()
    
except Exception as e:
    print(f"Error: {e}")