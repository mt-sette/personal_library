DROP TABLE IF EXISTS `loan`;
DROP TABLE IF EXISTS `friends`;
DROP TABLE IF EXISTS `books`;

CREATE TABLE books
(
    id     INT AUTO_INCREMENT PRIMARY KEY,
    title  VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);

CREATE TABLE friends
(
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(255) NOT NULL,
    phone VARCHAR(30) UNIQUE ,
    email varchar(255) UNIQUE
);

CREATE TABLE loan
(
    id          INT AUTO_INCREMENT PRIMARY KEY,
    book_id     INT NOT NULL,
    friend_id   INT NOT NULL,
    loan_date   DATE DEFAULT NOW(),
    due_date    DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (friend_id) REFERENCES friends (id)
);

-- Insert mock data for books
INSERT INTO books (title, author) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald'),
('To Kill a Mockingbird', 'Harper Lee'),
('1984', 'George Orwell'),
('Pride and Prejudice', 'Jane Austen'),
('The Hobbit', 'J.R.R. Tolkien'),
('The Catcher in the Rye', 'J.D. Salinger'),
('Moby Dick', 'Herman Melville'),
('War and Peace', 'Leo Tolstoy'),
('The Odyssey', 'Homer'),
('Brave New World', 'Aldous Huxley');

-- Insert mock data for friends
INSERT INTO friends (name, phone, email) VALUES
('Alice Johnson', '+1234567890', 'alice.johnson@example.com'),
('Bob Smith', '+1987654321', 'bob.smith@example.com'),
('Charlie Brown', '+1456789123', 'charlie.brown@example.com'),
('Diana Prince', '+1789123456', 'diana.prince@example.com'),
('Ethan Hunt', '+1321654987', 'ethan.hunt@example.com'),
('Fiona Green', '+1654987321', 'fiona.green@example.com'),
('George Wilson', '+1987321654', 'george.wilson@example.com'),
('Hannah Baker', '+1321456987', 'hannah.baker@example.com'),
('Ian Malcolm', '+1456123789', 'ian.malcolm@example.com'),
('Jane Doe', '+1789456123', 'jane.doe@example.com');
