CREATE DATABASE IF NOT EXISTS cset170final;
USE cset170final;

CREATE TABLE IF NOT EXISTS users (
	acc_num INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(300) NOT NULL,
    balance INT(255) NOT NULL DEFAULT 0,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    ssn VARCHAR(9) NOT NULL,
    phone_num VARCHAR(15),
    CONSTRAINT chk_ssn_9_chars CHECK (LENGTH(ssn) = 9)
);
ALTER TABLE users AUTO_INCREMENT=578060;

CREATE TABLE IF NOT EXISTS applications (
    appli_num INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    ssn VARCHAR(9) NOT NULL,
    phone_num VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS addresses (
    acc_num INT UNIQUE,
    appli_num INT UNIQUE,
    street_addr VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code INT NOT NULL,
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

-- CREATE TABLE IF NOT EXISTS loggedin (
--     acc_num INT,
--     admin_id INT,
--     FOREIGN KEY (acc_num) REFERENCES users(acc_num), 
--     FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
--     CHECK (acc_num IS NULL OR admin_id IS NULL)
-- );

CREATE TABLE IF NOT EXISTS loggedin (
    username VARCHAR(255),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    CHECK (username IS NULL OR admin_id IS NULL)
);
-- drop table loggedin;

INSERT INTO admin 
	(username, password)
VALUES
	("admin", "password");
    
INSERT INTO users (username, balance, first_name, last_name, phone_num, password, ssn) VALUES('ddzidzic', '95000', 'Daedalus', 'Dzidzic', '1234567890', 'password', '333222444');
INSERT INTO users (username, balance, first_name, last_name, phone_num, password, ssn) VALUES('ddzidzic', '12467', 'Daedalus', 'Dzidzic', '1234567890', 'password', '333222444');
INSERT INTO users (username, balance, first_name, last_name, phone_num, password, ssn) VALUES ('mmalova', '780000', 'Maya', 'Malova', '0987654321', 'password', '333222333');

INSERT INTO loggedin (username) VALUES('ddzidzic');
INSERT INTO addresses (acc_num, street_addr, city, state, zip_code) VALUES (1, '123 Example St.', 'City', 'PA', '12345');
select * from users;
select * from loggedin;
select * from addresses;

-- INSERT INTO loggedin 
-- VALUES (NULL, NULL);

-- drop database cset170final;