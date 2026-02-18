create database librarydb;
USE LibraryDB;

-- 1. Librarian table first
CREATE TABLE Librarian (
    librarian_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15)
);

-- 2. Members
CREATE TABLE Members (
    member_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(15)
);

-- 3. Book
CREATE TABLE Book (
    book_id INT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    librarian_id INT,
    FOREIGN KEY (librarian_id) REFERENCES Librarian(librarian_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 4. Transactions
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    book_id INT,
    member_id INT,
    librarian_id INT,
    date_issued DATE,
    due_date DATE,
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (librarian_id) REFERENCES Librarian(librarian_id)
);

-- Insert data
INSERT INTO Librarian VALUES
(1, 'Anita', '78906543'),
(2, 'Rahul Menon', '98765432'),
(3, 'Sneha Nair', '91234567'),
(4, 'Arjun Das', '99887766');

INSERT INTO Members VALUES
(201, 'Rahul', '9876543210'),
(202, 'Anjali', '9123456780'),
(203, 'Vishnu', '9988776655'),
(204, 'Meera', '9090909090');

INSERT INTO Book VALUES
(101, 'Database Systems', 'Korth', 1),
(102, 'Operating System Concepts', 'Silberschatz', 2),
(103, 'Computer Networks', 'Tanenbaum', 3),
(104, 'Artificial Intelligence', 'Stuart Russell', 4);

INSERT INTO Transactions VALUES
(1001, 101, 201, 1, '2026-02-15', '2026-03-01'),
(1002, 102, 202, 2, '2026-02-16', '2026-03-02'),
(1003, 103, 203, 3, '2026-02-17', '2026-03-03'),
(1004, 104, 204, 4, '2026-02-18', '2026-03-04'),
(1007, 104, 204, 4, '2025-12-25', '2026-01-01');

CREATE TABLE ADMIN(
	username varchar(50),
    password VARCHAR(50),
    name varchar(50),
    email VARCHAR(50));


SELECT * FROM Admin;

-- If no admin exists, insert manually:
INSERT INTO Admin (username, password, name, email) 
VALUES ('admin', 'abc1234', 'Admin', 'admin@library.com');

SELECT * FROM Book;
SELECT * FROM Librarian;
SELECT * FROM Members;
SELECT * FROM Transactions;