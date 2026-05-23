import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def test_vote_counts():
    print("=== Testing Vote Counts ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor(dictionary=True)
        
        # Query all candidates with vote counts
        query = "SELECT id, name, party, COALESCE(vote_count, 0) as vote_count FROM candidates ORDER BY vote_count DESC"
        cursor.execute(query)
        candidates = cursor.fetchall()
        
        print("Candidates and their vote counts:")
        print("-" * 50)
        for candidate in candidates:
            print(f"ID: {candidate['id']}, Name: {candidate['name']}, Party: {candidate['party']}, Votes: {candidate['vote_count']}")
        
        cursor.close()
        cnx.close()
        
        print("\n✅ Vote counts test completed successfully")
        
    except Exception as e:
        print(f"❌ Vote counts test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vote_counts()