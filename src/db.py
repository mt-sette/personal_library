from config import engine
from sqlalchemy import text



def _execute_query(query, params=None, select=True):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            out = connection.execute(text(query), params or {})
            if select:
                result = [row for row in out]
                transaction.commit()
                return result
            else:
                transaction.commit()
                return out.rowcount
        except Exception as e:
            transaction.rollback()
            raise e


def _get_all(table_name):
    query = f"SELECT * FROM {table_name};"
    return _execute_query(query)


## FRIENDS ##

def get_friends():
    return _get_all("friends")

def get_friend_by_name(name):
    query = "SELECT * FROM friends WHERE name REGEXP :name;"
    params = {"name": name}
    return _execute_query(query, params)

def add_friend(name, email, phone):
    query = "INSERT INTO friends (name, email, phone) VALUES (:name, :email, :phone);"
    params = {"name": name, "email": email, "phone": phone}
    rows = _execute_query(query, params, select=False)
    print(f"Added friend: {name} ({email}), {phone}, {rows} row(s) affected.")
    return rows

## BOOKS ##

def get_books():
    return _get_all("books")

def add_book(title, author):
    query = "INSERT INTO books (title, author) VALUES (:title, :author);"
    params = {"title": title, "author": author}
    rows = _execute_query(query, params, select=False)
    print(f"Added book: {title} by {author}, {rows} row(s) affected.")
    return rows
    
def find_books_by_title(title_pattern):
    query = "SELECT * FROM books WHERE title REGEXP :pattern;"
    params = {"pattern": title_pattern}
    return _execute_query(query, params)

## LOANS ##

def get_loans():
    return _get_all("loan")

def books_on_loan():
    query = """
    SELECT b.*, f.name AS friend_name, l.loan_date, l.return_date
    FROM books b
    JOIN loan l ON b.id = l.book_id
    JOIN friends f ON l.friend_id = f.id
    WHERE l.return_date IS NULL;
    """
    return _execute_query(query)

def add_loan(book_id, friend_id): 
    # check in the DB for active loan for this book
    check_query = "SELECT 1 FROM loan WHERE book_id = :book_id AND return_date IS NULL LIMIT 1;"
    exists = _execute_query(check_query, {"book_id": book_id})
    if exists:
        print(f"Book ID {book_id} is already on loan.")
        return False
    
    query = "INSERT INTO loan (book_id, friend_id) VALUES (:book_id, :friend_id);"
    params = {"book_id": book_id, "friend_id": friend_id}
    rows = _execute_query(query, params, select=False)
    print(f"Added loan: Book ID {book_id} to Friend ID {friend_id}, {rows} row(s) affected.")
    return rows

def update_book_return_date(loan_id, return_date):
    query = "UPDATE loan SET return_date = :return_date WHERE id = :loan_id;"
    params = {"return_date": return_date, "loan_id": loan_id}
    rows = _execute_query(query, params, select=False)
    print(f"Updated return date for loan ID {loan_id} to {return_date}, {rows} row(s) affected.")
    return rows