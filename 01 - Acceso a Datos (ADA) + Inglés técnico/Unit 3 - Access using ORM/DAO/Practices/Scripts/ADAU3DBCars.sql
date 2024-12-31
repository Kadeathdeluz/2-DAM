-- Script to create DB and tables ADAU3DBCars, and Racecars and Drivers 
-- Also to create the given user and gran privileges to him/her and to populate tables

CREATE DATABASE IF NOT EXISTS ADAU3DBCars CHARACTER SET utf8 COLLATE utf8_spanish_ci;
CREATE USER IF NOT EXISTS 'mavenuser'@'localhost' IDENTIFIED BY 'ada0486'; --
GRANT ALL PRIVILEGES ON ADAU3DBCars.* TO 'mavenuser'@'localhost';
USE ADAU3DBCars;
-- Create table of drivers
CREATE TABLE IF NOT EXISTS Drivers (
DNI VARCHAR(9),
name VARCHAR(40),
age INTEGER,
PRIMARY KEY(DNI)
);
-- Create table of race cars
CREATE TABLE IF NOT EXISTS Racecars (
carID VARCHAR(10),
brand VARCHAR(20),
price DOUBLE,
DNI VARCHAR(9),
PRIMARY KEY(carID),
FOREIGN KEY (DNI) REFERENCES Drivers (DNI)
);
INSERT INTO Drivers VALUES('11111111A','Carlos Sainz',30);
INSERT INTO Drivers VALUES('22222222F','Luis Moya',50);
INSERT INTO Drivers VALUES('12345678A','Ana Prost',27);
INSERT INTO Racecars VALUES('1111AAA','Toyota',30000,'11111111A');
INSERT INTO Racecars VALUES('2222EEE','Subaru',40000,'11111111A');
INSERT INTO Racecars VALUES('3333III', 'Renault', 25000, '12345678A');