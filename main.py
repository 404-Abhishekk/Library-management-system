# main.py
import tkinter as tk
from database import Database
from login_screens import LoginScreen
from admin_dashboard import AdminDashboard
from user_dashboard import UserDashboard
from utils import UIHelper

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        UIHelper.center_window(self.root)
        
        # Initialize database connection
        self.db = Database()
        if not self.db.connect():
            self.root.quit()
            return
        
        # Current user info
        self.current_member = None
        
        # Show main menu
        self.show_main_menu()
    
    def show_main_menu(self):
        # Clear the entire root window first
        UIHelper.clear_frame(self.root)
        
        # Create login screen with proper callbacks
        self.login_screen = LoginScreen(self.root, self.on_login_success, self.show_main_menu)
        self.login_screen.show_main_menu()
    
    def on_login_success(self, user_type, member=None):
        if user_type == "admin":
            self.show_admin_dashboard()
        else:
            self.current_member = member
            self.show_user_dashboard()
    
    def show_admin_dashboard(self):
        # AdminDashboard will clear the frame in its setup_dashboard
        self.admin_dashboard = AdminDashboard(self.root, self.show_main_menu)
    
    def show_user_dashboard(self):
        # UserDashboard will clear the frame in its setup_dashboard
        self.user_dashboard = UserDashboard(self.root, self.current_member, self.show_main_menu)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()