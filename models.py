# models.py
from database import Database
from datetime import date, timedelta

class BookModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Book")
    
    @staticmethod
    def get_by_id(book_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Book WHERE book_id = %s", (book_id,))
    
    @staticmethod
    def search(search_term, search_by="Title"):
        db = Database()
        if search_by == "Title":
            return db.fetch_all("SELECT * FROM Book WHERE title LIKE %s", (f"%{search_term}%",))
        else:
            return db.fetch_all("SELECT * FROM Book WHERE author LIKE %s", (f"%{search_term}%",))
    
    @staticmethod
    def add(book_id, title, author, librarian_id):
        db = Database()
        return db.execute_query(
            "INSERT INTO Book VALUES (%s, %s, %s, %s)",
            (book_id, title, author, librarian_id)
        )
    
    @staticmethod
    def update(book_id, title, author, librarian_id):
        db = Database()
        return db.execute_query(
            "UPDATE Book SET title=%s, author=%s, librarian_id=%s WHERE book_id=%s",
            (title, author, librarian_id, book_id)
        )
    
    @staticmethod
    def delete(book_id):
        db = Database()
        return db.execute_query("DELETE FROM Book WHERE book_id=%s", (book_id,))

class TransactionModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Transactions")
    
    @staticmethod
    def get_by_member(member_id):
        db = Database()
        return db.fetch_all("SELECT * FROM Transactions WHERE member_id = %s", (member_id,))
    
    @staticmethod
    def issue(trans_id, book_id, member_id, librarian_id):
        db = Database()
        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)
        return db.execute_query(
            "INSERT INTO Transactions VALUES (%s, %s, %s, %s, %s, %s)",
            (trans_id, book_id, member_id, librarian_id, issue_date, due_date)
        )
    
    @staticmethod
    def return_book(trans_id):
        db = Database()
        return db.execute_query("DELETE FROM Transactions WHERE transaction_id=%s", (trans_id,))
    
    @staticmethod
    def get_overdue():
        db = Database()
        today = date.today()
        return db.fetch_all("SELECT * FROM Transactions WHERE due_date < %s", (today,))

class LibrarianModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Librarian")
    
    @staticmethod
    def get_by_id(librarian_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Librarian WHERE librarian_id = %s", (librarian_id,))

class MemberModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Members")
    
    @staticmethod
    def get_by_id(member_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    
    @staticmethod
    def validate_login(member_id, name):
        db = Database()
        return db.fetch_one(
            "SELECT * FROM Members WHERE member_id = %s AND name = %s",
            (member_id, name)
        )
    
    @staticmethod
    def register(member_id, name, contact):
        db = Database()
        # Check if member_id already exists
        existing = db.fetch_one("SELECT * FROM Members WHERE member_id = %s", (member_id,))
        if existing:
            return False, "Member ID already exists"
        
        # Insert new member
        success = db.execute_query(
            "INSERT INTO Members (member_id, name, contact) VALUES (%s, %s, %s)",
            (member_id, name, contact)
        )
        if success:
            return True, "Member registered successfully"
        else:
            return False, "Registration failed"
    
    @staticmethod
    def get_next_member_id():
        db = Database()
        result = db.fetch_one("SELECT MAX(member_id) FROM Members")
        if result and result[0]:
            return result[0] + 1
        else:
            return 201

class AdminModel:
    @staticmethod
    def validate_login(username, password):
        db = Database()
        # Use the actual Admin table from database
        return db.fetch_one(
            "SELECT * FROM Admin WHERE username = %s AND password = %s",
            (username, password)
        )