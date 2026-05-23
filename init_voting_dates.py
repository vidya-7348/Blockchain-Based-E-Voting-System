import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="Database_API/.env")

def init_voting_dates_table():
    print("=== Initializing Voting Dates Table ===")
    
    try:
        # Connect to database
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        # Create voting_dates table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS voting_dates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            start_date DATETIME,
            end_date DATETIME,
            result_date DATETIME,
            result_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        print("Creating voting_dates table...")
        cursor.execute(create_table_query)
        
        # Check if table is empty and insert default data
        cursor.execute("SELECT COUNT(*) FROM voting_dates")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Inserting default voting dates...")
            insert_query = """
            INSERT INTO voting_dates (start_date, end_date, result_date, result_message)
            VALUES (%s, %s, %s, %s)
            """
            default_data = (
                '2025-12-01 00:00:00',
                '2025-12-31 23:59:59',
                '2026-01-01 00:00:00',
                'Check the results on {date}'
            )
            cursor.execute(insert_query, default_data)
        
        cnx.commit()
        print("✅ Voting dates table initialized successfully")
        
        # Verify the table structure
        cursor.execute("DESCRIBE voting_dates")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for column in columns:
            print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
        
        # Show sample data
        cursor.execute("SELECT * FROM voting_dates LIMIT 1")
        data = cursor.fetchone()
        if data:
            print(f"\nSample data: {data}")
        else:
            print("\nNo data found")
        
        cursor.close()
        cnx.close()
        
    except Exception as e:
        print(f"❌ Failed to initialize voting dates table: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_voting_dates_table()