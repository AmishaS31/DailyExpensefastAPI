CREATE DATABASE daily_expense;

USE daily_expense;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount INT NOT NULL
);