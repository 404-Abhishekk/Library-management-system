# utils.py
from tkinter import messagebox
from datetime import date

class FineCalculator:
    @staticmethod
    def calculate_fine(due_date, rate_per_day=10):
        today = date.today()
        if today > due_date:
            days_overdue = (today - due_date).days
            fine = days_overdue * rate_per_day
            return days_overdue, fine
        return 0, 0

class UIHelper:
    @staticmethod
    def center_window(window, width=None, height=None):
        window.update_idletasks()
        if width and height:
            window.geometry(f"{width}x{height}")
        w = window.winfo_width()
        h = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (w // 2)
        y = (window.winfo_screenheight() // 2) - (h // 2)
        window.geometry(f'+{x}+{y}')
    
    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_info(title, message):
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title, message):
        messagebox.showwarning(title, message)
    
    @staticmethod
    def ask_yes_no(title, message):
        return messagebox.askyesno(title, message)