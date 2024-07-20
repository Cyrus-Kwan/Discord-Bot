-- Create table to store bot configurations
CREATE TABLE IF NOT EXISTS bot_config (
    bot_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    bot_name TEXT NOT NULL, 
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    bot_description TEXT,
    access_token TEXT NOT NULL
    );

-- Insert initial bot configurations
INSERT INTO bot_config (bot_name, bot_description, access_token) VALUES
("cmd#7080" , "Modular discord bot that tracks users and performs moderation.", "MTI0ODU3Mjk2NTQ3ODQ2NTY2MA.GcvxrW.00NhBl0AWHSmX_nEH6-5UHxQcHXMYfeMRT0wNI");

-- Verify that the data has been inserted correctly
SELECT * FROM bot_config;