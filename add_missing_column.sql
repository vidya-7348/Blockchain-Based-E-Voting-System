USE voter_db_copy;

-- Add the missing has_voted column
ALTER TABLE users ADD COLUMN has_voted BOOLEAN DEFAULT FALSE;

-- Verify the table structure
DESCRIBE users;