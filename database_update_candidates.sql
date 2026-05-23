-- Database Schema Update Script for candidate photos and logos
-- This script adds support for storing candidate photos and party logos

USE voter_db_copy;

-- Add columns for candidate photos and party logos to the candidates table
-- (In a real implementation, you might store these in a separate table or use IPFS hashes)

-- Since candidates are stored on the blockchain, we don't need to create a candidates table
-- The blockchain handles candidate storage, and we only need to store user information in the database

-- However, if you want to store additional candidate information in the database, 
-- you could create a candidates table like this:

/*
CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blockchain_id INT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    party VARCHAR(255) NOT NULL,
    photo_hash VARCHAR(255),
    party_logo_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes for faster lookups
CREATE INDEX idx_blockchain_id ON candidates(blockchain_id);
CREATE INDEX idx_party ON candidates(party);
*/

-- In this implementation, we're using the blockchain to store candidate information
-- and only storing IPFS hashes or file paths in the blockchain
-- The actual files would be stored in a file system or IPFS network

-- Verify the current table structure
DESCRIBE users;
DESCRIBE voting_dates;