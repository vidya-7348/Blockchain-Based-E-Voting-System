CREATE TABLE IF NOT EXISTS voting_dates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATETIME,
    end_date DATETIME,
    result_date DATETIME,
    result_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert a default record if the table is empty
INSERT INTO voting_dates (start_date, end_date, result_date, result_message)
SELECT 
    '2025-12-01 00:00:00',
    '2025-12-31 23:59:59',
    '2026-01-01 00:00:00',
    'Check the results on {date}'
WHERE NOT EXISTS (
    SELECT 1 FROM voting_dates
);