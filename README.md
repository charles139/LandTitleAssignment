# LandTitleAssignment
Flask app with Python, MySQL and USPS web services API

Sprinkle in jQuery on the front end to handle ajax call to USPS zipCode lookup API


MySQL commands to help initialize the database

CREATE DATABASE landTitle_addressBook;

USE landTitle_addressBook;
CREATE TABLE addresses (id INT(11) AUTO_INCREMENT PRIMARY KEY ,
name VARCHAR(255),
address VARCHAR(255) ,
city VARCHAR(100) ,
state VARCHAR(50) ,
zip_code VARCHAR(15) ,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
INSERT INTO addresses
(name , address , city , state , zip_code)
VALUES(
'Charles Hollins',
'Street Address data',
'Palm Desert',
'California',
'92211');
