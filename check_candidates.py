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
    
    # Query candidates
    cursor.execute('SELECT * FROM candidates')
    results = cursor.fetchall()
    
    print('Candidates in database:')
    for row in results:
        print(row)
    
    cursor.close()
    cnx.close()
    
except Exception as e:
    print(f"Error: {e}")