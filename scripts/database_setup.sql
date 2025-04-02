CREATE DATABASE IF NOT EXISTS cset170final;
USE cset170final;

CREATE TABLE IF NOT EXISTS users (
	acc_num INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    balance INT NOT NULL DEFAULT 0,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    ssn VARCHAR(9) NOT NULL,
    phone_num INT,
    CONSTRAINT chk_ssn_9_chars CHECK (LENGTH(ssn) = 9)
);

CREATE TABLE IF NOT EXISTS applications (
    appli_num INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    ssn VARCHAR(9) NOT NULL,
    phone_num int
);

CREATE TABLE IF NOT EXISTS addresses (
    acc_num INT UNIQUE,
    appli_num INT UNIQUE,
    street_addr VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code INT NOT NULL,
    country VARCHAR(2) NOT NULL,
    FOREIGN KEY (acc_num) REFERENCES users(acc_num),
    FOREIGN KEY (appli_num) REFERENCES applications(appli_num)
);

CREATE TABLE IF NOT EXISTS admin (
	admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
-- If you ran the old admin table create and don't want to delete loggedin
-- ALTER TABLE admin ADD CONSTRAINT unique_username UNIQUE (username);

CREATE TABLE IF NOT EXISTS loggedin (
    acc_num INT,
    admin_id INT,
    FOREIGN KEY (acc_num) REFERENCES users(acc_num), 
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    CHECK (acc_num IS NULL OR admin_id IS NULL)
);

INSERT INTO admin 
	(username, password)
VALUES
	("admin", "password");

INSERT INTO loggedin 
VALUES (NULL, NULL);