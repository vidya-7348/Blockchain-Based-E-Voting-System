import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def check_candidates_table():
    print("=== Checking Candidates Table ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Check candidates table structure
        print("\n--- Candidates Table Structure ---")
        cursor.execute("DESCRIBE candidates")
        candidates_columns = cursor.fetchall()
        print("Columns:")
        for column in candidates_columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # Check if vote_count column exists
        vote_count_exists = any(column[0] == 'vote_count' for column in candidates_columns)
        print(f"\nvote_count column exists: {vote_count_exists}")
        
        # Get sample data
        print("\n--- Sample Candidates Data ---")
        cursor.execute("SELECT id, name, party, vote_count FROM candidates LIMIT 5")
        candidates = cursor.fetchall()
        if candidates:
            print("ID | Name | Party | Votes")
            print("-" * 40)
            for candidate in candidates:
                print(f"{candidate[0]} | {candidate[1]} | {candidate[2]} | {candidate[3] or 0}")
        else:
            print("No candidates found")
        
        cursor.close()
        cnx.close()
        
        print("\n✅ Candidates table check completed successfully")
        
    except Exception as e:
        print(f"❌ Candidates table check failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_candidates_table()