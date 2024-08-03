-- Create table to store bot configurations
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    client_name TEXT NOT NULL, 
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    client_description TEXT,
    access_token TEXT NOT NULL
    );