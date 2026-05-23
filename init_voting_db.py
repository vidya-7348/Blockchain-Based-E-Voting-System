import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

try:
    # Connect to database
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    cursor = cnx.cursor()
    
    print("[SUCCESS] Database connection successful!")
    
    # Create voting_dates table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS voting_dates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        start_date DATETIME NOT NULL,
        end_date DATETIME NOT NULL,
        result_date DATETIME NOT NULL,
        result_message VARCHAR(255) DEFAULT 'Check the results on {date}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    print("[SUCCESS] voting_dates table created or already exists!")
    
    # Add has_voted column to users table
    try:
        add_column_query = "ALTER TABLE users ADD COLUMN has_voted BOOLEAN DEFAULT FALSE"
        cursor.execute(add_column_query)
        print("[SUCCESS] has_voted column added to users table!")
    except mysql.connector.Error as err:
        if err.errno == 1060:  # Duplicate column name error
            print("[SUCCESS] has_voted column already exists in users table!")
        else:
            print(f"[ERROR] Error adding has_voted column: {err}")
    
    # Create index on has_voted for faster lookups
    try:
        create_index_query = "CREATE INDEX idx_has_voted ON users(has_voted)"
        cursor.execute(create_index_query)
        print("[SUCCESS] Index on has_voted column created!")
    except mysql.connector.Error as err:
        if err.errno == 1061:  # Duplicate key name error
            print("[SUCCESS] Index on has_voted column already exists!")
        else:
            print(f"[ERROR] Error creating index on has_voted column: {err}")
    
    # Commit changes
    cnx.commit()
    
    # Verify the table structure
    cursor.execute("DESCRIBE voting_dates")
    columns = cursor.fetchall()
    print("\n[INFO] voting_dates table structure:")
    for column in columns:
        print(f"  - {column[0]} ({column[1]})")
    
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    print("\n[INFO] users table structure:")
    for column in columns:
        print(f"  - {column[0]} ({column[1]})")
    
    cursor.close()
    cnx.close()
    
    print("\n[SUCCESS] Database initialization completed successfully!")
    
except Exception as e:
    print(f"[ERROR] Database initialization error: {e}")