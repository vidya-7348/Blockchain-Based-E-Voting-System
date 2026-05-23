-- Database Schema Update Script for voter_db_copy
-- This script adds the email field to the users table

USE voter_db_copy;

-- Add emailid column to users table (if not exists)
ALTER TABLE users ADD COLUMN emailid VARCHAR(255) UNIQUE AFTER contactNumber;

-- Create index on emailid for faster lookups
CREATE INDEX idx_emailid ON users(emailid);

-- Optional: Insert a sample admin user (replace with actual admin credentials)
-- INSERT INTO users (firstName, lastName, emailid, password, role) 
-- VALUES ('Admin', 'User', 'admin@voting.com', 'admin123', 'admin');

-- Verify the table structure
DESCRIBE users;
