# login_screens.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import UIHelper
from models import AdminModel, MemberModel

class LoginScreen:
    def __init__(self, parent, on_success, on_back=None):
        self.parent = parent
        self.on_success = on_success
        self.on_back = on_back  # Store the back callback
        self.frame = None
    
    def show_main_menu(self):
        if self.frame:
            self.frame.destroy()
        
        self.frame = tk.Frame(self.parent, bg='#f0f0f0')
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title = tk.Label(self.frame, text="Library Management System", 
                        font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(self.frame, text="Select User Type", 
                           font=('Arial', 14), bg='#f0f0f0', fg='#666')
        subtitle.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.frame, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        # Admin button
        admin_btn = tk.Button(button_frame, text="👤 Admin Login", 
                             command=self.show_admin_login,
                             font=('Arial', 14, 'bold'),
                             bg='#3498db', fg='white',
                             width=20, height=2,
                             bd=0, cursor='hand2')
        admin_btn.pack(pady=10)
        
        # User Login button
        user_btn = tk.Button(button_frame, text="👥 Member Login", 
                            command=self.show_user_login,
                            font=('Arial', 14, 'bold'),
                            bg='#2ecc71', fg='white',
                            width=20, height=2,
                            bd=0, cursor='hand2')
        user_btn.pack(pady=10)
        
        # Member Registration button
        register_btn = tk.Button(button_frame, text="📝 New Member Registration", 
                                command=self.show_member_registration,
                                font=('Arial', 14, 'bold'),
                                bg='#f39c12', fg='white',
                                width=20, height=2,
                                bd=0, cursor='hand2')
        register_btn.pack(pady=10)
        
        # Exit button
        exit_btn = tk.Button(button_frame, text="❌ Exit", 
                            command=self.parent.quit,
                            font=('Arial', 12),
                            bg='#e74c3c', fg='white',
                            width=15, height=1,
                            bd=0, cursor='hand2')
        exit_btn.pack(pady=20)
    
    def show_admin_login(self):
        UIHelper.clear_frame(self.frame)
        
        # Title
        tk.Label(self.frame, text="Admin Login", font=('Arial', 20, 'bold'), 
                bg='#f0f0f0', fg='#333').pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.frame, bg='white', relief='groove', bd=2)
        form_frame.pack(pady=20, padx=20)
        
        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 12), 
                bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.admin_username = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.admin_username.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 12), 
                bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.admin_password = tk.Entry(form_frame, font=('Arial', 12), width=30, show="*")
        self.admin_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Login", command=self.admin_login,
                 font=('Arial', 12), bg='#3498db', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Back", command=self.show_main_menu,
                 font=('Arial', 12), bg='#95a5a6', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
    
    def admin_login(self):
        username = self.admin_username.get()
        password = self.admin_password.get()
        
        admin = AdminModel.validate_login(username, password)
        if admin:
            self.on_success("admin")
        else:
            UIHelper.show_error("Login Failed", "Invalid username or password")
    
    def show_user_login(self):
        UIHelper.clear_frame(self.frame)
        
        tk.Label(self.frame, text="Member Login", font=('Arial', 20, 'bold'), 
                bg='#f0f0f0', fg='#333').pack(pady=20)
        
        form_frame = tk.Frame(self.frame, bg='white', relief='groove', bd=2)
        form_frame.pack(pady=20, padx=20)
        
        tk.Label(form_frame, text="Member ID:", font=('Arial', 12), 
                bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.user_id = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.user_id.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="Name:", font=('Arial', 12), 
                bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.user_name = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.user_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Link to registration
        link_frame = tk.Frame(form_frame, bg='white')
        link_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        tk.Label(link_frame, text="Not a member?", font=('Arial', 10), 
                bg='white').pack(side='left')
        tk.Button(link_frame, text="Register here", command=self.show_member_registration,
                 font=('Arial', 10, 'underline'), bg='white', fg='blue',
                 bd=0, cursor='hand2').pack(side='left')
        
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Login", command=self.user_login,
                 font=('Arial', 12), bg='#2ecc71', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Back", command=self.show_main_menu,
                 font=('Arial', 12), bg='#95a5a6', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
    
    def user_login(self):
        member_id = self.user_id.get()
        name = self.user_name.get()
        
        if not member_id or not name:
            UIHelper.show_warning("Warning", "Please enter both Member ID and Name")
            return
        
        member = MemberModel.validate_login(member_id, name)
        if member:
            self.on_success("user", member)
        else:
            UIHelper.show_error("Login Failed", "Invalid Member ID or Name")
    
    def show_member_registration(self):
        UIHelper.clear_frame(self.frame)
        
        # Title
        tk.Label(self.frame, text="New Member Registration", font=('Arial', 20, 'bold'), 
                bg='#f0f0f0', fg='#333').pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.frame, bg='white', relief='groove', bd=2)
        form_frame.pack(pady=20, padx=20)
        
        # Get next available member ID
        next_id = MemberModel.get_next_member_id()
        
        # Member ID (auto-suggested)
        tk.Label(form_frame, text="Member ID:", font=('Arial', 12), 
                bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.reg_member_id = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.reg_member_id.grid(row=0, column=1, padx=10, pady=10)
        self.reg_member_id.insert(0, str(next_id))
        self.reg_member_id.config(state='readonly')
        
        # Full Name
        tk.Label(form_frame, text="Full Name:", font=('Arial', 12), 
                bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.reg_name = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.reg_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Contact Number
        tk.Label(form_frame, text="Contact Number:", font=('Arial', 12), 
                bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.reg_contact = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.reg_contact.grid(row=2, column=1, padx=10, pady=10)
        
        # Confirm Contact
        tk.Label(form_frame, text="Confirm Contact:", font=('Arial', 12), 
                bg='white').grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.reg_contact_confirm = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.reg_contact_confirm.grid(row=3, column=1, padx=10, pady=10)
        
        # Terms and Conditions
        self.terms_var = tk.IntVar()
        tk.Checkbutton(form_frame, text="I agree to the library terms and conditions", 
                      variable=self.terms_var, bg='white', font=('Arial', 10)).grid(
                          row=4, column=0, columnspan=2, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Register", command=self.register_member,
                 font=('Arial', 12), bg='#2ecc71', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Clear", command=self.clear_registration_form,
                 font=('Arial', 12), bg='#f39c12', fg='white',
                 width=10, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Back to Login", command=self.show_user_login,
                 font=('Arial', 12), bg='#3498db', fg='white',
                 width=12, cursor='hand2').pack(side='left', padx=5)
    
    def clear_registration_form(self):
        self.reg_name.delete(0, tk.END)
        self.reg_contact.delete(0, tk.END)
        self.reg_contact_confirm.delete(0, tk.END)
        self.terms_var.set(0)
    
    def register_member(self):
        member_id = self.reg_member_id.get()
        name = self.reg_name.get().strip()
        contact = self.reg_contact.get().strip()
        contact_confirm = self.reg_contact_confirm.get().strip()
        
        if not name:
            UIHelper.show_warning("Validation Error", "Please enter your full name")
            return
        
        if not contact:
            UIHelper.show_warning("Validation Error", "Please enter your contact number")
            return
        
        if contact != contact_confirm:
            UIHelper.show_warning("Validation Error", "Contact numbers do not match")
            return
        
        if len(contact) < 10 or not contact.isdigit():
            UIHelper.show_warning("Validation Error", "Please enter a valid 10-digit contact number")
            return
        
        if self.terms_var.get() == 0:
            UIHelper.show_warning("Validation Error", "Please accept the terms and conditions")
            return
        
        success, message = MemberModel.register(member_id, name, contact)
        
        if success:
            UIHelper.show_info("Registration Successful", 
                              f"{message}\n\nYour Member ID is: {member_id}\nPlease remember this ID for login.")
            self.clear_registration_form()
            self.show_user_login()
        else:
            UIHelper.show_error("Registration Failed", message)