CREATE DATABASE ADAU3DBCompany CHARACTER SET utf8 COLLATE utf8_spanish_ci;
CREATE USER 'mavenuser'@'localhost' IDENTIFIED BY 'ada0486'; --
GRANT ALL PRIVILEGES ON ADAU3DBCompany.* TO 'mavenuser'@'localhost';
USE ADAU3DBCompany;
-- Create the employee's table
CREATE TABLE Employee (
taxID VARCHAR(9),
firstname VARCHAR(100),
lastname VARCHAR(100),
salary DECIMAL(9,2),
CONSTRAINT emp_tid_pk PRIMARY KEY (taxID)
);
-- Insert random employees
INSERT INTO Employee (taxID, firstname, lastname, salary) VALUES ('11111111A', 'José', 'Salcedo
López', 1279.90);
INSERT INTO Employee (taxID, firstname, lastname, salary) VALUES ('22222222B', 'Juan', 'De la
Fuente Arqueros', 1100.73);
INSERT INTO Employee (taxID, firstname, lastname, salary) VALUES ('33333333C', 'Antonio', 'Bosch
Jericó', 1051.45);
INSERT INTO Employee (taxID, firstname, lastname, salary) VALUES ('44444444D', 'Ana', 'Sanchís
Torres', 1300.02);
INSERT INTO Employee (taxID, firstname, lastname, salary) VALUES ('55555555E', 'Isabel', 'Martí
Navarro', 1051.45);