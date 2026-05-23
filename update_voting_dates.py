import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def update_voting_dates():
    print("=== Updating Voting Dates ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Update voting dates to past dates so results will be visible
        update_query = """
        UPDATE voting_dates 
        SET start_date = %s, end_date = %s, result_date = %s
        WHERE id = 1
        """
        
        # Set dates to past dates
        past_dates = (
            '2025-01-01 00:00:00',  # Start date (past)
            '2025-11-30 23:59:59',  # End date (past)
            '2025-12-01 00:00:00'   # Result date (past)
        )
        
        print("Updating voting dates to past dates...")
        cursor.execute(update_query, past_dates)
        
        # Check if update was successful
        if cursor.rowcount > 0:
            print("✅ Voting dates updated successfully")
        else:
            print("⚠️  No rows updated. Inserting new record...")
            # If no rows were updated, insert a new record
            insert_query = """
            INSERT INTO voting_dates (start_date, end_date, result_date, result_message)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (*past_dates, 'Check the results on {date}'))
            print("✅ New voting dates record inserted")
        
        cnx.commit()
        
        # Verify the update
        cursor.execute("SELECT * FROM voting_dates WHERE id = 1")
        data = cursor.fetchone()
        if data:
            print(f"\nUpdated data: {data}")
        else:
            print("\nNo data found")
        
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print(f"❌ Failed to update voting dates: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_voting_dates()