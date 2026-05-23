import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing database connection...")
print(f"Host: {os.environ.get('MYSQL_HOST', 'Not set')}")
print(f"User: {os.environ.get('MYSQL_USER', 'Not set')}")
print(f"Database: {os.environ.get('MYSQL_DB', 'Not set')}")

try:
    cnx = mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB'],
    )
    print("✅ Database connection successful!")
    cnx.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")