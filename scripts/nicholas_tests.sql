USE cset170final;

SELECT * FROM users;
SELECT * FROM applications;
SELECT * FROM addresses;
SELECT * FROM admin;
SELECT * FROM loggedin;
DESC applications;
DESC addresses;

INSERT INTO applications     
	(username, password, first_name, last_name, ssn, phone_num)
VALUES ('newaccccccccc', 'newacc', 'New',  'Account', '123456789', 7177896789);

ALTER TABLE admin ADD CONSTRAINT unique_username UNIQUE (username);

INSERT INTO users 
	(username, password, balance, first_name, last_name, ssn)
VALUES 
	-- ("bluemario8", "blue", 5, "nicholas", "N", "001352532"),
	-- ("steve43", "stev", 0, "Steve", "Smith", "999999999"),
    ("bill", "pass", 0, "Bill", "Stevens", "09");
    
INSERT INTO applications
	(username, password, first_name, last_name, ssn)
VALUES
	("Jim", "power", "Jim", "Browning", "91043251");
    
INSERT INTO addresses
	(acc_num, appli_num, street_addr, city, state, zip_code, country)
VALUES
	(1, NULL, "123 Street St.", "Street City", "New York", 12345, "US");
    
    
    
    