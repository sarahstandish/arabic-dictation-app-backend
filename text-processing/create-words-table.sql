-- boilerplate to create a new table for words

CREATE TABLE words (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    voweled_word VARCHAR(50) NOT NULL,
    unvoweled_word VARCHAR(50) NOT NULL
);