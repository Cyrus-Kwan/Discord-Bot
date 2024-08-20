--Table that stores substring states as an adjacency list
CREATE TABLE IF NOT EXISTS graph (
    current TEXT,
    previous TEXT,
    edge INTEGER,
    probability DECIMAL(size, 2)
)