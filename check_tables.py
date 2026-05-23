import mysql.connector
import os
from dotenv import load_dotenv
from typing import Any

# Load environment variables
load_dotenv()

try:
    # Connect to database
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    cursor = cnx.cursor()
    
    # Show all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        table_name = str(table[0])
        print(f"  - {table_name}")
        
        # Show table structure
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        print(f"    Structure:")
        for column in columns:
            column_name = str(column[0])
            column_type = str(column[1])
            print(f"      - {column_name} ({column_type})")
        print()
    
    cursor.close()
    cnx.close()
    
except Exception as e:
    print(f"Error: {e}")