import tkinter as tk
import re

from tkinter import messagebox, ttk
from .utils import center_window, setup_text_widget_editing

class RegistrationWindow(tk.Tk):
    """The user registration window. Allows users to create a new account"""
    def __init__(self, db_manager, open_login_func):
        super().__init__()
        self.db_manager = db_manager
        self.open_login_func = open_login_func

        self.width = 476
        self.height = 306
        center_window(self, self.width, self.height)
        self.resizable(False, False)
        self.title("Registration")
        
        self.ui_font = ("Verdana", 10)
        # Labels #
        self.registration_title_label = tk.Label(self, font=("Verdana", 12), text="Реєстрація")
        self.login_label = tk.Label(self, font=self.ui_font, text="Логін:")
        self.email_label = tk.Label(self, font=self.ui_font, text="Електронна пошта:")
        self.password_label = tk.Label(self, font=self.ui_font, text="Пароль:")
        self.password_repeat_label = tk.Label(self, font=self.ui_font, text="Підтвердити Пароль:")
        
        # Entries #
        self.entry_width = 30
        
        self.login_entry = tk.Entry(self, width=self.entry_width, font=self.ui_font)
        setup_text_widget_editing(self.login_entry)
        
        self.email_entry = tk.Entry(self, width=self.entry_width, font=self.ui_font)
        setup_text_widget_editing(self.email_entry)
        
        self.password_entry = tk.Entry(self, width=self.entry_width, font=self.ui_font, show="*")
        setup_text_widget_editing(self.password_entry)
        
        self.password_repeat_entry = tk.Entry(self, width=self.entry_width, font=self.ui_font, show="*")
        setup_text_widget_editing(self.password_repeat_entry)
        
        # Buttons #
        self.buttons_width = 12
        
        self.login_button = tk.Button(self, width=self.buttons_width, height=1, font=self.ui_font, text="Назад до Входу", command=self.go_to_login)
        self.registration_button = tk.Button(self, width=self.buttons_width, height=1, font=self.ui_font, text="Зареєструватись", command=self.submit_registration)
        
        # Location of Widgets #
        self.registration_title_label.grid(row=0, column=0, columnspan=2, sticky="n", padx=5, pady=10)
        self.login_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.email_label.grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.password_label.grid(row=3, column=0, sticky="w", padx=5, pady=10)
        self.password_repeat_label.grid(row=4, column=0, sticky="w", padx=5, pady=10)
        
        self.login_entry.grid(row=1, column=1, sticky="w", padx=5, pady=10)
        self.email_entry.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        self.password_entry.grid(row=3, column=1, sticky="w", padx=5, pady=10)
        self.password_repeat_entry.grid(row=4, column=1, sticky="w", padx=5, pady=10)
        
        self.login_button.grid(row=5, column=0, sticky="e", padx=5, pady=20)
        self.registration_button.grid(row=5, column=1, sticky="e", padx=5, pady=20)
        
        self.login_entry.bind("<Return>", lambda event: self.email_entry.focus_set())
        self.email_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self.password_repeat_entry.focus_set())
        self.password_repeat_entry.bind("<Return>", lambda event: self.submit_registration())
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def submit_registration(self):
        """Validates user input and attempts to register the user via the DatabaseManager"""
        messagebox_title = "Реєстрація"

        username = self.login_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        password_repeat = self.password_repeat_entry.get()

        if not all([username, email, password, password_repeat]):
            messagebox.showwarning(messagebox_title, "Будь ласка, заповніть усі поля.", parent=self)
            return

        min_username_len = 4
        max_username_len = 16
        username_pattern = f"^[a-zA-Z0-9_-]{{{min_username_len},{max_username_len}}}$"
        if not re.fullmatch(username_pattern, username):
            messagebox.showwarning(
                messagebox_title,
                f"Логін повинен містити від {min_username_len} до {max_username_len} символів.\n"
                "Дозволені символи: латинські літери (a-z, A-Z), цифри (0-9), "
                "знаки підкреслення (_) та дефіс (-).",
                parent=self
            )
            self.login_entry.focus_set()
            return

        email_pattern_basic = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(email_pattern_basic, email) or not email.isascii():
            messagebox.showwarning(
                messagebox_title,
                "Будь ласка, введіть дійсну адресу електронної пошти, використовуючи лише латинські літери, цифри та стандартні символи (@ . _ % + -).",
                parent=self
            )
            self.email_entry.focus_set()
            return

        min_password_len = 8
        if len(password) < min_password_len:
            messagebox.showwarning(messagebox_title, f"Пароль повинен містити щонайменше {min_password_len} символів.", parent=self)
            self.password_entry.delete(0, tk.END)
            self.password_repeat_entry.delete(0, tk.END)
            self.password_entry.focus_set()
            return

        if not all(32 <= ord(char) <= 126 for char in password):
             messagebox.showwarning(messagebox_title, "Пароль може містити лише латинські літери, цифри та стандартні символи (~!@#$%^&*()_+=-`...).", parent=self)
             self.password_entry.delete(0, tk.END)
             self.password_repeat_entry.delete(0, tk.END)
             self.password_entry.focus_set()
             return

        if password != password_repeat:
            messagebox.showerror(messagebox_title, "Паролі не співпадають.", parent=self)
            self.password_entry.delete(0, tk.END)
            self.password_repeat_entry.delete(0, tk.END)
            self.password_entry.focus_set()
            return

        print(f"UI: Attempting to register user: {username}")
        if self.db_manager.register_user(username, email, password):
            messagebox.showinfo(messagebox_title, "Реєстрація успішна! Тепер ви можете увійти.", parent=self)
            self.go_to_login()
        else:
            pass
        
    def go_to_login(self):
        """Destroy self and call the function to open login window"""
        self.destroy()
        self.open_login_func()
            
    def on_close(self):
        """Close the window"""
        print("Closing Registration Window...")
        self.destroy()
        