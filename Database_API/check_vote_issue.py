import os
import mysql.connector
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
    
    print("=" * 60)
    print("CHECKING VOTING SYSTEM SETUP")
    print("=" * 60)
    
    # Check users table structure
    print("\n1. USERS TABLE STRUCTURE:")
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[0]} ({col[1]})")
    
    # Check if voterId column exists
    column_names = [col[0] for col in columns]
    if 'voterId' not in column_names:
        print("\n❌ ERROR: 'voterId' column is MISSING from users table!")
        print("   This is likely causing the voting error.")
    else:
        print("\n✅ voterId column exists")
    
    if 'has_voted' not in column_names:
        print("❌ ERROR: 'has_voted' column is MISSING from users table!")
    else:
        print("✅ has_voted column exists")
    
    # Check sample user data
    print("\n2. SAMPLE USER DATA:")
    cursor.execute("SELECT emailid, voterId, has_voted FROM users LIMIT 3")
    users = cursor.fetchall()
    for user in users:
        print(f"   Email: {user[0]}, VoterID: {user[1]}, Has Voted: {user[2]}")
    
    # Check candidates
    print("\n3. CANDIDATES TABLE:")
    cursor.execute("SELECT COUNT(*) FROM candidates")
    count = cursor.fetchone()[0]
    print(f"   Total candidates: {count}")
    
    if count > 0:
        cursor.execute("SELECT id, name FROM candidates LIMIT 3")
        candidates = cursor.fetchall()
        for cand in candidates:
            print(f"   - ID: {cand[0]}, Name: {cand[1]}")
    else:
        print("   ❌ WARNING: No candidates found!")
    
    cursor.close()
    cnx.close()
    
    print("\n" + "=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
