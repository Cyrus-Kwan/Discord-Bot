--Table that stores substring states as an adjacency list
CREATE TABLE IF NOT EXISTS Graph (
    Current TEXT,
    Previous TEXT,
    Edge INTEGER,
    Probability REAL,
    PRIMARY KEY (Current, Previous)
);