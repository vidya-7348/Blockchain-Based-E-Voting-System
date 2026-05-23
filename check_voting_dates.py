import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def check_voting_dates():
    print("=== Checking Current Voting Dates ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Get the current voting dates
        cursor.execute("SELECT * FROM voting_dates WHERE id = 1")
        data = cursor.fetchone()
        
        if data:
            print("Current voting dates record:")
            print(f"ID: {data[0]}")
            print(f"Start Date: {data[1]}")
            print(f"End Date: {data[2]}")
            print(f"Result Date: {data[3]}")
            print(f"Result Message: {data[4]}")
            print(f"Created At: {data[5]}")
            print(f"Updated At: {data[6]}")
            
            # Check if result date has passed
            result_date = data[3]
            current_date = datetime.now()
            print(f"\nCurrent system date: {current_date}")
            print(f"Has result date passed? {current_date >= result_date}")
        else:
            print("No voting dates record found")
        
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print(f"❌ Failed to check voting dates: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_voting_dates()