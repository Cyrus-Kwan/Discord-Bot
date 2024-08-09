-- Table that stores user messages for language model training
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY,
    channel_id INTEGER, 
    content TEXT,
    reply BOOLEAN,
    respondent INTEGER,
    author TEXT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP
);