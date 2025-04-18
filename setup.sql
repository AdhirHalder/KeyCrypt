-- 📁 setup.sql
-- 👇 Creates database and table needed for KeyCrypt

CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    second_password_hash TEXT NOT NULL
);
