-- Store basic user information WIP
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    global_name TEXT,
    display_name TEXT,
    created_at DATETIME
);