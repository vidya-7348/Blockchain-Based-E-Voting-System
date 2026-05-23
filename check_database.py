import mysql.connector
import os
from dotenv import load_dotenv

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
    
    print("✅ Database connection successful!")
    
    # Check if email column exists
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    print("\n📋 Current users table structure:")
    for column in columns:
        print(f"  - {column[0]} ({column[1]})")
    
    # Check if email column exists
    email_exists = any('emailid' in column for column in columns)
    if email_exists:
        print("\n✅ Email column (emailid) exists!")
    else:
        print("\n❌ Email column (emailid) does NOT exist!")
        print("You need to run the database update script:")
        print("mysql -u your_username -p voter_db_copy < database_update.sql")
    
    # Check admin users
    cursor.execute("SELECT firstName, lastName, emailid, role FROM users WHERE role = 'admin'")
    admin_users = cursor.fetchall()
    print(f"\n👨‍💼 Admin users found: {len(admin_users)}")
    for admin in admin_users:
        print(f"  - {admin[0]} {admin[1]} ({admin[2]}) - {admin[3]}")
    
    cursor.close()
    cnx.close()
    
except Exception as e:
    print(f"❌ Database error: {e}")
