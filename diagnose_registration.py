import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def diagnose_database():
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
        print("\n--- DATABASE TABLES ---")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            table_name = str(table[0])
            print(f"  - {table_name}")
            
            # Show table structure
            print(f"    Structure of {table_name}:")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            for column in columns:
                column_name = str(column[0])
                column_type = str(column[1])
                is_nullable = str(column[2])
                key_info = str(column[3])
                default_value = str(column[4]) if column[4] else "NULL"
                extra_info = str(column[5]) if column[5] else ""
                print(f"      - {column_name} ({column_type}) {is_nullable} {key_info} DEFAULT:{default_value} {extra_info}")
            print()
        
        # Test inserting a sample user
        print("--- TESTING USER INSERTION ---")
        try:
            # Check if users table exists
            cursor.execute("SHOW TABLES LIKE 'users'")
            result = cursor.fetchone()
            if not result:
                print("❌ Users table does not exist!")
                return
            
            # Try to insert a test user
            test_query = """
            INSERT INTO users 
            (firstName, middleName, lastName, emailid, password, voterId, contactNumber, aadhar, dob, age, gender, address, role, has_voted) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            test_values = (
                "Test",           # firstName
                "Middle",         # middleName
                "User",           # lastName
                "test@example.com", # emailid
                "password123",    # password
                "VID001",         # voterId
                "1234567890",     # contactNumber
                "123456789012",   # aadhar
                "2000-01-01",     # dob
                25,               # age
                "Male",           # gender
                "Test Address",   # address
                "user",           # role
                0                 # has_voted
            )
            
            cursor.execute(test_query, test_values)
            cnx.commit()
            print("✅ Test user inserted successfully!")
            
            # Delete the test user
            cursor.execute("DELETE FROM users WHERE emailid = %s", ("test@example.com",))
            cnx.commit()
            print("✅ Test user cleaned up!")
            
        except mysql.connector.Error as e:
            print(f"❌ Database error during test insertion: {e}")
            print(f"Error code: {e.errno}")
            print(f"SQLSTATE: {e.sqlstate}")
            print(f"Message: {e.msg}")
        except Exception as e:
            print(f"❌ Unexpected error during test insertion: {e}")
        
        cursor.close()
        cnx.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
        print(f"Error code: {e.errno}")
        if e.errno == 1045:
            print("  This usually means the username or password is incorrect.")
        elif e.errno == 2003:
            print("  This usually means MySQL server is not running or host/port is incorrect.")
        elif e.errno == 1049:
            print("  This usually means the database doesn't exist.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    diagnose_database()