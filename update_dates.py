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
    
    # Update voting dates to past dates so results will be shown
    # Set result date to December 1, 2025 (which is in the past now)
    update_query = """
        UPDATE voting_dates 
        SET start_date = %s, end_date = %s, result_date = %s, result_message = %s 
        WHERE id = %s
    """
    
    # Use dates in the past so results will be displayed
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 11, 30, 23, 59, 59)
    result_date = datetime(2025, 12, 1)  # This is in the past now
    result_message = "Check the results on {date}"
    record_id = 1
    
    cursor.execute(update_query, (start_date, end_date, result_date, result_message, record_id))
    cnx.commit()
    
    print("Voting dates updated successfully!")
    
    # Verify the update
    cursor.execute('SELECT * FROM voting_dates')
    results = cursor.fetchall()
    
    print('Updated voting dates table contents:')
    for row in results:
        print(row)
    
    cursor.close()
    cnx.close()
    
except Exception as e:
    print(f"Error: {e}")