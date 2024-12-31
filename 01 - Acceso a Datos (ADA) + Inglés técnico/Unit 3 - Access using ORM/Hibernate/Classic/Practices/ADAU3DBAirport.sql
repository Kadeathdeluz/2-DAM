-- Script to create DB ADAU3DBAirport and tables Airport, Neighbour, Airplanetype and Airplane
-- Also to create the given user and gran privileges to him/her
CREATE DATABASE IF NOT EXISTS ADAU3DBAirport CHARACTER SET utf8mb4 COLLATE utf8mb4_es_0900_ai_ci;

CREATE USER IF NOT EXISTS mavenuser@localhost IDENTIFIED BY 'ada0486'; --
GRANT ALL PRIVILEGES ON ADAU3DBAirport.* to mavenuser@localhost;

USE ADAU3DBAirport;

-- Table Airport
CREATE TABLE IF NOT EXISTS Airport (
airportID   VARCHAR(3) PRIMARY KEY,
capacity    INTEGER
);

-- Table Neighbour
CREATE TABLE IF NOT EXISTS Neighbour (
airportIDA  VARCHAR(3),
airportIDB  VARCHAR(3),
PRIMARY KEY (airportIDA, airportIDB),
CONSTRAINT FOREIGN KEY nei_ida_fk (airportIDA) REFERENCES Airport(airportID),
CONSTRAINT FOREIGN KEY nei_idb_fk (airportIDB) REFERENCES Airport(airportID)
);

-- Table Airplanetype
CREATE TABLE IF NOT EXISTS Airplanetype (
name    VARCHAR(255) PRIMARY KEY,
size    INTEGER
);

-- Table Airplane
CREATE TABLE IF NOT EXISTS Airplane (
regno       INTEGER PRIMARY KEY,
airportID   VARCHAR(3),
typename    VARCHAR(255),
CONSTRAINT air_ida_fk FOREIGN KEY (airportID) REFERENCES Airport(airportID),
CONSTRAINT air_typ_fk FOREIGN KEY (typename) REFERENCES Airplanetype(name)
);