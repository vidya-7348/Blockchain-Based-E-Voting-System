import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_table_structure():
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
        
        # Show all tables
        print("\n=== DATABASE TABLES ===")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            table_name = str(table[0])
            print(f"\nTable: {table_name}")
            
            # Show table structure
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print(f"  Columns:")
            required_columns = ['firstName', 'middleName', 'lastName', 'emailid', 'password', 'voterId', 'contactNumber', 'aadhar', 'dob', 'age', 'gender', 'address', 'role', 'has_voted']
            existing_columns = [str(column[0]) for column in columns]
            
            for column in columns:
                column_name = str(column[0])
                column_type = str(column[1])
                is_nullable = str(column[2])
                key_info = str(column[3])
                default_value = str(column[4]) if column[4] else "NULL"
                extra_info = str(column[5]) if column[5] else ""
                status = "✅" if column_name in required_columns else "ℹ️"
                print(f"    {status} {column_name} ({column_type}) {is_nullable} {key_info} DEFAULT:{default_value} {extra_info}")
            
            # Check for missing required columns
            missing_columns = [col for col in required_columns if col not in existing_columns]
            if missing_columns:
                print(f"  ❌ Missing required columns: {missing_columns}")
            else:
                print(f"  ✅ All required columns present")
        
        # Check a sample row if users table exists
        print("\n=== SAMPLE DATA CHECK ===")
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"Users table has {count} rows")
            
            if count > 0:
                cursor.execute("SELECT * FROM users LIMIT 1")
                sample_row = cursor.fetchone()
                print("Sample row data:")
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                for i, column in enumerate(columns):
                    column_name = str(column[0])
                    value = sample_row[i] if sample_row[i] is not None else "NULL"
                    print(f"  {column_name}: {value}")
        except mysql.connector.Error as e:
            print(f"No users table or empty table: {e}")
        
        cursor.close()
        cnx.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    check_table_structure()