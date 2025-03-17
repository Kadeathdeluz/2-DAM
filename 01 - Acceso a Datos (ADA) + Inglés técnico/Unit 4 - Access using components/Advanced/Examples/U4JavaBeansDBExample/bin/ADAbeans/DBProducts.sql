CREATE DATABASE DBProducts;

-- Create a user if you are using MySQL 5.7 or MySQL 8 or newer
CREATE USER 'mavenuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'ada0486';
GRANT ALL PRIVILEGES ON DBProducts.* TO 'mavenuser'@'localhost';

USE DBProducts;

CREATE TABLE products (
idp     INTEGER,
name    VARCHAR(20),
CONSTRAINT pro_idp_pk PRIMARY KEY (idp)
);

INSERT INTO products VALUES (1, "Duruss Cobalt");
INSERT INTO products VALUES (2, "Varlion Avant Carbon");
INSERT INTO products VALUES (3, "Star Vie Pyramid R50");
INSERT INTO products VALUES (4, "Dunlop Titan");
INSERT INTO products VALUES (5, "Vision King jm");
INSERT INTO products VALUES (6, "Slazenger Reflex Pro");

CREATE TABLE orders (
ido     INTEGER AUTO_INCREMENT,
idp     INTEGER,
amount  INTEGER,
CONSTRAINT ord_ido_pk PRIMARY KEY (ido),
CONSTRAINT ord_idp_fk FOREIGN KEY (idp) REFERENCES products(idp)
);
