import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_users_table():
    try:
        # Connect to database
        print("Connecting to database...")
        cnx = mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB'],
        )
        cursor = cnx.cursor()
        
        print("✅ Database connection successful!")
        
        # List of required columns and their definitions
        required_columns = {
            'middleName': 'VARCHAR(255)',
            'aadhar': 'VARCHAR(12)',
            'dob': 'DATE',
            'age': 'INT',
            'gender': 'VARCHAR(10)',
            'address': 'TEXT',
            'has_voted': 'BOOLEAN DEFAULT FALSE',
            'emailid': 'VARCHAR(255) UNIQUE'
        }
        
        # Check existing columns
        cursor.execute("DESCRIBE users")
        existing_columns = [str(column[0]) for column in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns
        for column_name, column_definition in required_columns.items():
            if column_name not in existing_columns:
                try:
                    query = f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"
                    cursor.execute(query)
                    print(f"✅ Added column: {column_name}")
                except mysql.connector.Error as e:
                    print(f"ℹ️  Column {column_name} may already exist or error occurred: {e}")
            else:
                print(f"✅ Column already exists: {column_name}")
        
        # Create indexes
        indexes = [
            ("idx_emailid", "emailid"),
            ("idx_voterid", "voterId"),
            ("idx_has_voted", "has_voted")
        ]
        
        for index_name, column_name in indexes:
            try:
                query = f"CREATE INDEX {index_name} ON users({column_name})"
                cursor.execute(query)
                print(f"✅ Created index: {index_name}")
            except mysql.connector.Error as e:
                print(f"ℹ️  Index {index_name} may already exist or error occurred: {e}")
        
        # Commit changes
        cnx.commit()
        
        # Show final table structure
        print("\n=== FINAL TABLE STRUCTURE ===")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for column in columns:
            column_name = str(column[0])
            column_type = str(column[1])
            is_nullable = str(column[2])
            key_info = str(column[3])
            default_value = str(column[4]) if column[4] else "NULL"
            extra_info = str(column[5]) if column[5] else ""
            print(f"  {column_name} ({column_type}) {is_nullable} {key_info} DEFAULT:{default_value} {extra_info}")
        
        cursor.close()
        cnx.close()
        
        print("\n✅ Users table update completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    update_users_table()