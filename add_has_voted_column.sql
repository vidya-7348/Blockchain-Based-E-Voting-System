-- Add the missing has_voted column to the users table
USE voter_db_copy;
ALTER TABLE users ADD COLUMN has_voted BOOLEAN DEFAULT FALSE;

-- Verify the table structure
DESCRIBE users;