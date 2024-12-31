-- Script to create DB ADAU3DBTaxinspectors (for AT3) and tables Office, Inspector, Taxpayer and Taxfile
CREATE DATABASE IF NOT EXISTS ADAU3DBTaxinspectors CHARACTER SET utf8mb4 COLLATE
utf8mb4_es_0900_ai_ci;
CREATE USER IF NOT EXISTS 'mavenuser'@'localhost' IDENTIFIED BY 'ada0486'; --
GRANT ALL PRIVILEGES ON ADAU3DBTaxinspectors.* to 'mavenuser'@'localhost';
USE ADAU3DBTaxinspectors;
-- Office
CREATE TABLE IF NOT EXISTS Office (
code VARCHAR(5) PRIMARY KEY,
city VARCHAR(100)
);
-- Inspector
CREATE TABLE IF NOT EXISTS Inspector (
dni VARCHAR(9) PRIMARY KEY,
firstname VARCHAR(30),
lastname VARCHAR(80),
birthday DATE,
commission DECIMAL(5,2),
code VARCHAR(5) NOT NULL,
CONSTRAINT ins_off_fk FOREIGN KEY (code) REFERENCES Office(code) ON UPDATE CASCADE,
CONSTRAINT ins_com_ck CHECK (commission BETWEEN 0 AND 30)
);
-- Taxpayer
CREATE TABLE Taxpayer (
nif VARCHAR(9) PRIMARY KEY,
fullname VARCHAR(110) NOT NULL,
address VARCHAR(150),
telephone VARCHAR(12)
);
-- Taxfile
CREATE TABLE Taxfile (
inspdni VARCHAR(9),
taxpaynif VARCHAR(9),
PRIMARY KEY (inspdni, taxpaynif),
CONSTRAINT taxf_dni_fk FOREIGN KEY (inspdni) REFERENCES Inspector(dni) ON DELETE CASCADE,
CONSTRAINT taxf_nif_fk FOREIGN KEY (taxpaynif) REFERENCES Taxpayer(nif) ON DELETE CASCADE
);