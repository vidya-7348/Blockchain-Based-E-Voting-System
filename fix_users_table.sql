-- Fix Users Table Structure for Registration
-- This script ensures all required columns exist for user registration

USE voter_db_copy;

-- Add missing columns to users table (IF NOT EXISTS is supported in MySQL 8.0+)
-- For older versions, we'll use ALTER TABLE ADD COLUMN wrapped in error handling

-- Add middleName column
ALTER TABLE users ADD COLUMN middleName VARCHAR(255);

-- Add aadhar column
ALTER TABLE users ADD COLUMN aadhar VARCHAR(12);

-- Add dob column
ALTER TABLE users ADD COLUMN dob DATE;

-- Add age column
ALTER TABLE users ADD COLUMN age INT;

-- Add gender column
ALTER TABLE users ADD COLUMN gender VARCHAR(10);

-- Add address column
ALTER TABLE users ADD COLUMN address TEXT;

-- Add has_voted column (might already exist)
ALTER TABLE users ADD COLUMN has_voted BOOLEAN DEFAULT FALSE;

-- Ensure emailid column exists and is unique (might already exist)
ALTER TABLE users ADD COLUMN emailid VARCHAR(255) UNIQUE;

-- Create indexes for better performance (will silently fail if they already exist)
CREATE INDEX idx_emailid ON users(emailid);
CREATE INDEX idx_voterid ON users(voterId);
CREATE INDEX idx_has_voted ON users(has_voted);

-- Verify the table structure
DESCRIBE users;