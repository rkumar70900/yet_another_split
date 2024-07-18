create database splitwise_api;

USE splitwise_api;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    user_id INT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE splits (
    split_id INT AUTO_INCREMENT PRIMARY KEY,
    expense_id INT,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES expenses(expense_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE friends (
    user_id INT,
    friend_user_id INT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (friend_user_id) REFERENCES users(user_id),
    PRIMARY KEY (user_id, friend_user_id)
);

INSERT INTO users (name, email) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Davis', 'charlie@example.com'),
('Diana Evans', 'diana@example.com'),
('Evan Foster', 'evan@example.com');

INSERT INTO expenses (description, amount, user_id) VALUES
('Lunch at cafe', 25.50, 1),
('Office supplies', 40.00, 2),
('Team outing', 150.75, 3),
('Project materials', 60.20, 4),
('Conference tickets', 200.00, 5);

drop table friends;

INSERT INTO friends (user_id, friend_user_id) VALUES
(1, 2),
(2, 1),
(1, 3),
(3, 1),
(2, 3),
(3, 2),
(2, 4),
(4, 2),
(3, 4),
(4, 3),
(3, 5),
(5, 3),
(4, 5),
(5, 4);

INSERT INTO splits (expense_id, user_id, amount) VALUES
(1, 1, 8.5),
(1, 2, 8.5),
(1, 3, 8.5),
(2, 2, 13.33),
(2, 3, 13.33),
(2, 4, 13.33),
(3, 3, 50.25),
(3, 4, 50.25),
(3, 5, 50.25),
(4, 3, 20.06),
(4, 4, 20.06),
(4, 5, 20.06),
(5, 3, 66.66),
(5, 4, 66.66),
(5, 5, 66.66);



