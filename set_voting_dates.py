import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

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
    
    # Check if there are any records in voting_dates table
    cursor.execute("SELECT COUNT(*) FROM voting_dates")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert a new record if table is empty
        print("No records found in voting_dates table. Inserting new record...")
        today = datetime.now().date()
        result_datetime = datetime.combine(today, datetime.strptime("11:00", "%H:%M").time())
        
        query = """
            INSERT INTO voting_dates (start_date, end_date, result_date, result_message) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (None, None, result_datetime, 'Election results are now available!'))
        print("Inserted new record with result date:", result_datetime)
    else:
        # Update existing record
        print(f"Found {count} records in voting_dates table. Updating the latest record...")
        today = datetime.now().date()
        result_datetime = datetime.combine(today, datetime.strptime("11:00", "%H:%M").time())
        
        query = """
            UPDATE voting_dates 
            SET result_date = %s, result_message = 'Election results are now available!'
            ORDER BY id DESC 
            LIMIT 1
        """
        cursor.execute(query, (result_datetime,))
        print("Updated record with result date:", result_datetime)
    
    # Commit the changes
    cnx.commit()
    
    # Verify the update
    cursor.execute("SELECT * FROM voting_dates ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    print(f"Current record in database: {result}")
    
    cursor.close()
    cnx.close()
    
    print("Voting dates updated successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()