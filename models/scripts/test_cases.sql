-- Create tables to store test data
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    release_date DATE NOT NULL,
    score INTEGER
);

CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    purchase_date DATE NOT NULL,
    price INTEGER NOT NULL
);

-- Populate tables with test data
INSERT INTO movies (title, release_date, score) VALUES 
("Deadpool & Wolverine", "2024-07-25", 8),
("Inside Out 2", "2024-06-13", 9),
("Fly Me to the Moon", "2024-07-11", 7),
("The Garfield Movie", "2024-05-30", 5),
("The Watchers", "2024-06-06", 3);

INSERT INTO people (first_name, last_name, age, gender) VALUES 
("Rachel", "Green", 32, "f"),
("Monica", "Geller", 27, "f"),
("Pheobe", "Hannigan", 34, "f"),
("Joseph", "Tribbiani", 34, "m"),
("Chandler", "Bing", 29, "m"),
("Ross", "Geller", 35, "m");

INSERT INTO sales (customer_id, movie_id, purchase_date, price) VALUES
(1, 3, "2024-07-11", 39),
(4, 2, "2024-06-15", 42),
(3, 1, "2024-07-28", 23),
(1, 2, "2024-06-23", 42),
(2, 5, "2024-07-03", 34);