import tkinter as tk
from tkinter import messagebox
from pc1_timer import TimerApplication

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC1 - Login")
        self.root.geometry("300x200")
        self.root.configure(bg='cyan')
        
        # Login credentials
        self.valid_username = "admin"
        self.valid_password = "password"
        
        self.create_login_widgets()
        
    def create_login_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Login", font=("Arial", 16, "bold"), bg='cyan')
        title_label.pack(pady=20)
        
        # Username
        tk.Label(self.root, text="Login ID:", bg='cyan').pack()
        self.username_entry = tk.Entry(self.root, width=20)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(self.root, text="Password:", bg='cyan').pack()
        self.password_entry = tk.Entry(self.root, width=20, show="*")
        self.password_entry.pack(pady=5)
        
        # Login Button
        login_btn = tk.Button(self.root, text="Login", command=self.login, 
                             bg='green', fg='white', font=("Arial", 10, "bold"))
        login_btn.pack(pady=20)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == self.valid_username and password == self.valid_password:
            self.root.destroy()
            # Launch main timer application
            app = TimerApplication()
            app.run()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")