USE voter_db_copy;

-- Show all tables
SHOW TABLES;

-- Describe users table
DESCRIBE users;

-- Check if voting_dates table exists
DESCRIBE voting_dates;

-- Check a sample row if users table exists
SELECT COUNT(*) FROM users;

-- Show a sample row
SELECT * FROM users LIMIT 1;