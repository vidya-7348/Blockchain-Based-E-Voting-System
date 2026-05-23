-- Database Schema Update Script for voting dates and results
-- This script adds tables for voting dates and results

USE voter_db_copy;

-- Create voting_dates table
CREATE TABLE IF NOT EXISTS voting_dates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    result_date DATETIME NOT NULL,
    result_message VARCHAR(255) DEFAULT 'Check the results on {date}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add has_voted column to users table
ALTER TABLE users ADD COLUMN has_voted BOOLEAN DEFAULT FALSE;

-- Create index on has_voted for faster lookups
CREATE INDEX idx_has_voted ON users(has_voted);

-- Verify the table structure
DESCRIBE voting_dates;
DESCRIBE users;