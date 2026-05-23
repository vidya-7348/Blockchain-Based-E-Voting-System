#!/usr/bin/env python3
"""Initialize candidates table in database"""
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
    
    print("✅ Database connection successful!")
    
    # Create candidates table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS candidates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        blockchain_id INT UNIQUE,
        name VARCHAR(255) NOT NULL,
        party VARCHAR(255) NOT NULL,
        photo_hash VARCHAR(500),
        party_logo_hash VARCHAR(500),
        vote_count INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_name_party (name, party)
    )
    """
    
    cursor.execute(create_table_query)
    print("✅ candidates table created or already exists!")
    
    # Add vote_count column if it doesn't exist (for existing tables)
    try:
        add_column_query = "ALTER TABLE candidates ADD COLUMN vote_count INT DEFAULT 0"
        cursor.execute(add_column_query)
        print("✅ vote_count column added to candidates table!")
    except mysql.connector.Error as e:
        if "Duplicate column name" in str(e):
            print("ℹ️ vote_count column already exists")
        else:
            raise
    
    # Commit changes
    cnx.commit()
    
    # Verify the table structure
    cursor.execute("DESCRIBE candidates")
    columns = cursor.fetchall()
    print("\n📋 candidates table structure:")
    for column in columns:
        print(f"  - {column[0]} ({column[1]})")
    
    cursor.close()
    cnx.close()
    
    print("\n✅ Candidates table initialization completed successfully!")
    
except Exception as e:
    print(f"❌ Database initialization error: {e}")


