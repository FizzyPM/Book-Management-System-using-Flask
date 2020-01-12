# Book Management System

Made with Python and JavaScript. 

1) Create a virtual environment and install the following packages:
 ```
 Flask, flask_session, sqlalchemy, requests, psycopg2
 ```
 
2) Install **postgresql** and Add the following tables to the database:
```
CREATE TABLE users (
    username VARCHAR(30) PRIMARY KEY,
    fname VARCHAR(30),
	lname VARCHAR(30),
    password VARCHAR(30) NOT NULL
);
CREATE TABLE ratings (
    uname VARCHAR(30) ,
    isbn VARCHAR(30),
	rating INT,
	review VARCHAR(60),
	foo BOOLEAN DEFAULT '0',
	CONSTRAINT pk_ratings PRIMARY KEY (uname,isbn)
);
CREATE TABLE cur_book (
    cur_isbn VARCHAR(30),
    cur_tite VARCHAR(30)
);
CREATE TABLE books (
    isbn_no VARCHAR(60) PRIMARY KEY,
    title VARCHAR(60) NOT NULL,
    author VARCHAR(60) NOT NULL,
    year INT NOT NULL
);
```
3) Execute the following commands to run the server:
```
$ export FLASK_APP=application.py
$ flask run
```
