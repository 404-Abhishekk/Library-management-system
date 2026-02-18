# admin_dashboard.py
import tkinter as tk
from tkinter import ttk
from models import BookModel, TransactionModel, LibrarianModel, MemberModel
from utils import UIHelper, FineCalculator
from datetime import date

class AdminDashboard:
    def __init__(self, parent, on_logout):
        self.parent = parent
        self.on_logout = on_logout
        self.notebook = None
        self.setup_dashboard()
    
    def setup_dashboard(self):
        # Clear parent
        UIHelper.clear_frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.create_book_management_tab()
        self.create_transaction_log_tab()
        self.create_fine_calculation_tab()
        self.create_librarian_management_tab()
        self.create_member_management_tab()
        
        # Logout button
        logout_btn = tk.Button(self.parent, text="Logout", command=self.on_logout,
                              font=('Arial', 10), bg='#e74c3c', fg='white',
                              cursor='hand2')
        logout_btn.pack(pady=5)
    
    def create_book_management_tab(self):
        book_tab = ttk.Frame(self.notebook)
        self.notebook.add(book_tab, text="📚 Book Management")
        
        # Title
        tk.Label(book_tab, text="Book Management System", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Form frame
        form_frame = tk.LabelFrame(book_tab, text="Book Details", font=('Arial', 12))
        form_frame.pack(pady=10, padx=20, fill='x')
        
        # Book ID
        tk.Label(form_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.book_id_entry = tk.Entry(form_frame, width=20)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Title
        tk.Label(form_frame, text="Title:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.book_title_entry = tk.Entry(form_frame, width=30)
        self.book_title_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Author
        tk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.book_author_entry = tk.Entry(form_frame, width=20)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Librarian ID
        tk.Label(form_frame, text="Librarian ID:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.book_librarian_entry = tk.Entry(form_frame, width=20)
        self.book_librarian_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Add Book", command=self.add_book,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Book", command=self.update_book,
                 bg='#f39c12', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Book", command=self.delete_book,
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_book_form,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Search frame
        search_frame = tk.LabelFrame(book_tab, text="Search Books", font=('Arial', 12))
        search_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(search_frame, text="Search by:").pack(side='left', padx=5)
        self.search_var = tk.StringVar(value="Title")
        tk.Radiobutton(search_frame, text="Title", variable=self.search_var, 
                      value="Title").pack(side='left', padx=5)
        tk.Radiobutton(search_frame, text="Author", variable=self.search_var, 
                      value="Author").pack(side='left', padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_books,
                 bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Refresh", command=self.load_books,
                 bg='#95a5a6', fg='white').pack(side='left', padx=5)
        
        # Treeview for books
        tree_frame = tk.Frame(book_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.book_tree = ttk.Treeview(tree_frame, columns=('ID', 'Title', 'Author', 'Librarian'), 
                                       show='headings', height=15)
        self.book_tree.heading('ID', text='Book ID')
        self.book_tree.heading('Title', text='Title')
        self.book_tree.heading('Author', text='Author')
        self.book_tree.heading('Librarian', text='Librarian ID')
        
        self.book_tree.column('ID', width=80)
        self.book_tree.column('Title', width=250)
        self.book_tree.column('Author', width=200)
        self.book_tree.column('Librarian', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        self.book_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.book_tree.bind('<<TreeviewSelect>>', self.on_book_select)
        
        # Load books
        self.load_books()
    
    def load_books(self):
        for row in self.book_tree.get_children():
            self.book_tree.delete(row)
        
        books = BookModel.get_all()
        for book in books:
            self.book_tree.insert('', 'end', values=book)
    
    def search_books(self):
        search_term = self.search_entry.get()
        search_by = self.search_var.get()
        
        if not search_term:
            self.load_books()
            return
        
        for row in self.book_tree.get_children():
            self.book_tree.delete(row)
        
        books = BookModel.search(search_term, search_by)
        for book in books:
            self.book_tree.insert('', 'end', values=book)
    
    def add_book(self):
        book_id = self.book_id_entry.get()
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        librarian_id = self.book_librarian_entry.get()
        
        if not all([book_id, title, author, librarian_id]):
            UIHelper.show_warning("Warning", "Please fill all fields")
            return
        
        if BookModel.add(book_id, title, author, librarian_id):
            UIHelper.show_info("Success", "Book added successfully")
            self.load_books()
            self.clear_book_form()
    
    def update_book(self):
        selected = self.book_tree.selection()
        if not selected:
            UIHelper.show_warning("Warning", "Please select a book to update")
            return
        
        book_id = self.book_id_entry.get()
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        librarian_id = self.book_librarian_entry.get()
        
        if not all([book_id, title, author, librarian_id]):
            UIHelper.show_warning("Warning", "Please fill all fields")
            return
        
        if BookModel.update(book_id, title, author, librarian_id):
            UIHelper.show_info("Success", "Book updated successfully")
            self.load_books()
            self.clear_book_form()
    
    def delete_book(self):
        selected = self.book_tree.selection()
        if not selected:
            UIHelper.show_warning("Warning", "Please select a book to delete")
            return
        
        if UIHelper.ask_yes_no("Confirm", "Are you sure you want to delete this book?"):
            book_id = self.book_tree.item(selected[0])['values'][0]
            if BookModel.delete(book_id):
                UIHelper.show_info("Success", "Book deleted successfully")
                self.load_books()
                self.clear_book_form()
    
    def clear_book_form(self):
        self.book_id_entry.delete(0, tk.END)
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_librarian_entry.delete(0, tk.END)
    
    def on_book_select(self, event):
        selected = self.book_tree.selection()
        if selected:
            book = self.book_tree.item(selected[0])['values']
            self.clear_book_form()
            self.book_id_entry.insert(0, book[0])
            self.book_title_entry.insert(0, book[1])
            self.book_author_entry.insert(0, book[2])
            self.book_librarian_entry.insert(0, book[3])
    
    def create_transaction_log_tab(self):
        trans_tab = ttk.Frame(self.notebook)
        self.notebook.add(trans_tab, text="📋 Transaction Log")
        
        tk.Label(trans_tab, text="Issue/Return Books", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Form frame
        form_frame = tk.LabelFrame(trans_tab, text="Transaction Details", font=('Arial', 12))
        form_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(form_frame, text="Transaction ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.trans_id_entry = tk.Entry(form_frame, width=15)
        self.trans_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Book ID:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.trans_book_entry = tk.Entry(form_frame, width=15)
        self.trans_book_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.trans_member_entry = tk.Entry(form_frame, width=15)
        self.trans_member_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Librarian ID:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.trans_librarian_entry = tk.Entry(form_frame, width=15)
        self.trans_librarian_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Issue Book", command=self.issue_book,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Return Book", command=self.return_book,
                 bg='#f39c12', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_transactions,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Treeview for transactions
        tree_frame = tk.Frame(trans_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.trans_tree = ttk.Treeview(tree_frame, 
                                        columns=('ID', 'Book', 'Member', 'Librarian', 'Issued', 'Due'), 
                                        show='headings', height=15)
        self.trans_tree.heading('ID', text='Trans ID')
        self.trans_tree.heading('Book', text='Book ID')
        self.trans_tree.heading('Member', text='Member ID')
        self.trans_tree.heading('Librarian', text='Librarian ID')
        self.trans_tree.heading('Issued', text='Issue Date')
        self.trans_tree.heading('Due', text='Due Date')
        
        for col in ('ID', 'Book', 'Member', 'Librarian', 'Issued', 'Due'):
            self.trans_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=scrollbar.set)
        
        self.trans_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_transactions()
    
    def issue_book(self):
        trans_id = self.trans_id_entry.get()
        book_id = self.trans_book_entry.get()
        member_id = self.trans_member_entry.get()
        librarian_id = self.trans_librarian_entry.get()
        
        if not all([trans_id, book_id, member_id, librarian_id]):
            UIHelper.show_warning("Warning", "Please fill all fields")
            return
        
        if TransactionModel.issue(trans_id, book_id, member_id, librarian_id):
            due_date = date.today() + timedelta(days=14)
            UIHelper.show_info("Success", f"Book issued successfully!\nDue Date: {due_date}")
            self.load_transactions()
            self.clear_trans_form()
    
    def return_book(self):
        selected = self.trans_tree.selection()
        if not selected:
            UIHelper.show_warning("Warning", "Please select a transaction to return")
            return
        
        trans_id = self.trans_tree.item(selected[0])['values'][0]
        
        if UIHelper.ask_yes_no("Confirm", "Mark this book as returned?"):
            # Get transaction details for fine calculation
            trans = TransactionModel.get_by_member(trans_id)  # This needs adjustment
            if trans:
                due_date = trans[0][5]  # Assuming first transaction, due_date is at index 5
                days_overdue, fine = FineCalculator.calculate_fine(due_date)
                
                if fine > 0:
                    UIHelper.show_info("Fine", f"Book is {days_overdue} days overdue.\nFine amount: ${fine}")
            
            if TransactionModel.return_book(trans_id):
                UIHelper.show_info("Success", "Book returned successfully")
                self.load_transactions()
    
    def load_transactions(self):
        for row in self.trans_tree.get_children():
            self.trans_tree.delete(row)
        
        transactions = TransactionModel.get_all()
        for trans in transactions:
            self.trans_tree.insert('', 'end', values=trans)
    
    def clear_trans_form(self):
        self.trans_id_entry.delete(0, tk.END)
        self.trans_book_entry.delete(0, tk.END)
        self.trans_member_entry.delete(0, tk.END)
        self.trans_librarian_entry.delete(0, tk.END)
    
    def create_fine_calculation_tab(self):
        fine_tab = ttk.Frame(self.notebook)
        self.notebook.add(fine_tab, text="💰 Fine Calculation")
        
        tk.Label(fine_tab, text="Fine Calculator", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tk.Label(fine_tab, text="Check overdue books and calculate fines", 
                font=('Arial', 12)).pack(pady=5)
        
        tk.Button(fine_tab, text="Calculate All Fines", command=self.calculate_all_fines,
                 bg='#e74c3c', fg='white', font=('Arial', 12), 
                 width=20, height=2).pack(pady=10)
        
        # Results frame
        results_frame = tk.LabelFrame(fine_tab, text="Overdue Books", font=('Arial', 12))
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.fine_tree = ttk.Treeview(results_frame, 
                                      columns=('Trans ID', 'Book ID', 'Member ID', 'Due Date', 'Days Overdue', 'Fine'), 
                                      show='headings', height=10)
        
        self.fine_tree.heading('Trans ID', text='Transaction ID')
        self.fine_tree.heading('Book ID', text='Book ID')
        self.fine_tree.heading('Member ID', text='Member ID')
        self.fine_tree.heading('Due Date', text='Due Date')
        self.fine_tree.heading('Days Overdue', text='Days Overdue')
        self.fine_tree.heading('Fine', text='Fine Amount ($)')
        
        for col in ('Trans ID', 'Book ID', 'Member ID', 'Due Date', 'Days Overdue', 'Fine'):
            self.fine_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.fine_tree.yview)
        self.fine_tree.configure(yscrollcommand=scrollbar.set)
        
        self.fine_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def calculate_all_fines(self):
        for row in self.fine_tree.get_children():
            self.fine_tree.delete(row)
        
        overdue_books = TransactionModel.get_overdue()
        total_fine = 0
        
        for trans in overdue_books:
            due_date = trans[5]
            days_overdue, fine = FineCalculator.calculate_fine(due_date)
            total_fine += fine
            
            self.fine_tree.insert('', 'end', values=(
                trans[0], trans[1], trans[2], due_date, days_overdue, f"${fine}"
            ))
        
        if overdue_books:
            UIHelper.show_info("Fine Summary", f"Total fines to collect: ${total_fine}")
        else:
            UIHelper.show_info("Fine Summary", "No overdue books found!")
    
    def create_librarian_management_tab(self):
        lib_tab = ttk.Frame(self.notebook)
        self.notebook.add(lib_tab, text="👤 Librarians")
        
        tk.Label(lib_tab, text="Librarian Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(lib_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.lib_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Contact'), 
                                      show='headings', height=15)
        self.lib_tree.heading('ID', text='Librarian ID')
        self.lib_tree.heading('Name', text='Name')
        self.lib_tree.heading('Contact', text='Contact')
        
        self.lib_tree.column('ID', width=100)
        self.lib_tree.column('Name', width=200)
        self.lib_tree.column('Contact', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.lib_tree.yview)
        self.lib_tree.configure(yscrollcommand=scrollbar.set)
        
        self.lib_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_librarians()
    
    def load_librarians(self):
        librarians = LibrarianModel.get_all()
        for lib in librarians:
            self.lib_tree.insert('', 'end', values=lib)
    
    def create_member_management_tab(self):
        member_tab = ttk.Frame(self.notebook)
        self.notebook.add(member_tab, text="👥 Members")
        
        tk.Label(member_tab, text="Member Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(member_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.member_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Contact'), 
                                         show='headings', height=15)
        self.member_tree.heading('ID', text='Member ID')
        self.member_tree.heading('Name', text='Name')
        self.member_tree.heading('Contact', text='Contact')
        
        self.member_tree.column('ID', width=100)
        self.member_tree.column('Name', width=200)
        self.member_tree.column('Contact', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        
        self.member_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_members()
    
    def load_members(self):
        members = MemberModel.get_all()
        for member in members:
            self.member_tree.insert('', 'end', values=member)