--Table that stores substring states as an adjacency list
CREATE TABLE IF NOT EXISTS Graph (
    Current TEXT,
    previous TEXT,
    Edge INTEGER,
    Probability REAL(2),
    PRIMARY KEY (Current, previous)
);

DROP TRIGGER IF EXISTS Probability_on_insert;
DROP TRIGGER IF EXISTS Probability_on_update;

CREATE TRIGGER Probability_on_insert
AFTER INSERT ON Graph
FOR EACH ROW
BEGIN
    -- Update the probability for all rows with the same current node
    UPDATE Graph
    SET Probability = Edge / (
        SELECT SUM(Edge)
        FROM Graph
        WHERE Current = NEW.Current
    )
    WHERE Current = NEW.Current;
END;

CREATE TRIGGER Probability_on_update
AFTER UPDATE ON Graph
FOR EACH ROW
BEGIN
    -- Update the probability for all rows with the same current node
    UPDATE Graph
    SET Probability = Edge / (
        SELECT SUM(Edge)
        FROM Graph
        WHERE Current = NEW.Current
    )
    WHERE Current = NEW.Current;
END;