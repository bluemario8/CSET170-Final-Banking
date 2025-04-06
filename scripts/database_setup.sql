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
    username VARCHAR(50) UNIQUE,
    appli_num INT UNIQUE,
    street_addr VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code INT NOT NULL,
    FOREIGN KEY (appli_num) REFERENCES applications(appli_num)
);

CREATE TABLE IF NOT EXISTS admin (
	admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS loggedin (
    username VARCHAR(255),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    CHECK (username IS NULL OR admin_id IS NULL)
);
-- drop table loggedin;

CREATE TABLE IF NOT EXISTS transactions (
	transaction_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    acc_num INT NOT NULL,
    type VARCHAR(8),
    related_acc INT NOT NULL,
    amount INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(100),
    FOREIGN KEY (acc_num) REFERENCES users(acc_num),
    FOREIGN KEY (related_acc) REFERENCES users(acc_num)
);

INSERT INTO admin 
	(username, password)
VALUES
	("admin", "$+&091dmk_qdRDR@$+50_;oDiieR`~8D2q//KP=RR=88_=*G5KREqdko5Jk$;k9+533K;2`Eo;J/G`@_d35G&kqqdE@=P1`+PDeP0+=?LP;k*2$m2DK23E?_L+RR/E&`GJq13q=k+oid1o59iL0!8/5D0EKLo/*5$=R@;32_?2?dP`=Rk_iD`/J+Pq~8~oi2R8dG9K;i?P9?=#~L?k0*@i=+`159mG`@~&_m9i8$@k*9!mi?o3");
-- admin password is 'password'

INSERT INTO users (username, password, balance, first_name, last_name, ssn, phone_num)
	VALUES ('ddzidzic', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
			0, 'Daedalus', 'Dzidzic', '000000000', 1112223333),
            ('ddzidzic', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
			0, 'Daedalus', 'Dzidzic', '000000000', 1112223333),
            ('spetocs', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Sujay', 'Petocs', '333333333', 4445556666),
            ('mmalova', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Maya', 'Malova', '111111111', 2223334444),
            ('mmalova', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Maya', 'Malova', '111111111', 2223334444),
            ('dpolakova', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Darina', 'Polakova', '222222222', 3334445555),
            ('spetocs', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Sujay', 'Petocs', '333333333', 4445556666),
            ('spetocs', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Sujay', 'Petocs', '333333333', 4445556666),
            ('ddzidzic', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
			0, 'Daedalus', 'Dzidzic', '000000000', 1112223333),
            ('dpolakova', '$+&2q9e~*$1+JR=G_#K$8`!_/k~9?3#oEJ/`dLe*D$5?_GR#kPEk2JK2;kdE8#$2mmd/=G5#EK0dR=$3RG18L20J0~q;Q`#2`0~=e@Gq_`2@+JRDQ5i/3~*;L`95&@mq/D=1`ei&D*~kQKdKR1d+$k2R!5m2_RQo_L=KQ5@J$=@93R~2i`;#J`1J8Km`#*`D@11qq_o/&Q`+e`&3?`EDio9?*K55iL82Pm`;&o1/GJi@_mo/DQ',
            0, 'Darina', 'Polakova', '222222222', 3334445555);
-- all user passwords are TestPass01!

INSERT INTO addresses (username, street_addr, city, state, zip_code)
VALUES ('ddzidzic', '54 Sunshine Avenue', 'Belltown', 'AZ', '86118'),
		('mmalova', '162 Valley Street', 'Gap', 'PA', '17535'),
        ('dpolakova', '1955 Jana Drive', 'Clarksville', 'TN', '37042'),
        ('spetocs', '270 North Whealkate Drive', 'South Range', 'MI', '49963');

INSERT INTO loggedin (username, admin_id) VALUES (NULL, NULL);

select * from users;
select * from loggedin;
select * from addresses;
select * from transactions;

-- UPDATE loggedin SET username = NULL, admin_id = NULL;

-- drop database cset170final;