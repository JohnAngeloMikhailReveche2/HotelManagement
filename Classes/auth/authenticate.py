import sqlite3
import os
from tkinter import messagebox

class Authenticator:
    def __init__(self, username_var, password_var):
        self.username_var = username_var
        self.password_var = password_var

    def authenticate(self):
        username = self.username_var
        password = self.password_var

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Username and password are required.")
            return False, None

        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = """
                SELECT * FROM STAFF
                WHERE Username = ? AND Password = ? AND IsDeleted = 0
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                messagebox.showinfo("Success", f"Welcome, {username}!")
                return True, user
            else:
                messagebox.showerror("Invalid", "Incorrect username or password.")
                return False, None

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return False, None

