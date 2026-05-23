import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def test_database_connection():
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Test query to check if candidates table exists
        query = "SELECT COUNT(*) FROM candidates"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"Successfully connected to database. Found {count} candidates in the table.")
        
        # Test query to check if users table exists
        query = "SELECT COUNT(*) FROM users"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"Found {count} users in the table.")
        
        cursor.close()
        cnx.close()
        
        print("Database connection test passed!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()