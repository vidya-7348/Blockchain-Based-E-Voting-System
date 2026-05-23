import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def test_database_schema():
    print("=== Database Schema Test ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Check users table structure
        print("\n--- Users Table ---")
        cursor.execute("DESCRIBE users")
        users_columns = cursor.fetchall()
        print("Columns:")
        for column in users_columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # Check candidates table structure
        print("\n--- Candidates Table ---")
        cursor.execute("DESCRIBE candidates")
        candidates_columns = cursor.fetchall()
        print("Columns:")
        for column in candidates_columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # Check voting_dates table structure
        print("\n--- Voting Dates Table ---")
        cursor.execute("DESCRIBE voting_dates")
        voting_dates_columns = cursor.fetchall()
        print("Columns:")
        for column in voting_dates_columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # Check sample data
        print("\n--- Sample Data ---")
        
        # Count users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"Users: {user_count}")
        
        # Count candidates
        cursor.execute("SELECT COUNT(*) FROM candidates")
        candidate_count = cursor.fetchone()[0]
        print(f"Candidates: {candidate_count}")
        
        # Get first user (if exists)
        if user_count > 0:
            cursor.execute("SELECT emailid, voterId, has_voted FROM users LIMIT 1")
            user_sample = cursor.fetchone()
            print(f"Sample user: {user_sample}")
        
        # Get first candidate (if exists)
        if candidate_count > 0:
            cursor.execute("SELECT id, name, party FROM candidates LIMIT 1")
            candidate_sample = cursor.fetchone()
            print(f"Sample candidate: {candidate_sample}")
        
        cursor.close()
        cnx.close()
        
        print("\n✅ Database schema test completed successfully")
        
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_schema()