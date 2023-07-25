from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import string
import pyperclip
import sqlite3

# Generate a random password
def generate_password():
    password_length = password_length_var.get()
    password_characters = ""
    if include_uppercase_var.get():
        password_characters += string.ascii_uppercase
    if include_lowercase_var.get():
        password_characters += string.ascii_lowercase
    if include_digits_var.get():
        password_characters += string.digits
    if include_special_chars_var.get():
        password_characters += string.punctuation

    if not password_characters:
        messagebox.showerror("Password Manager", "Please select at least one option for password generation!")
        return

    password = ''.join(random.choice(password_characters) for _ in range(password_length))
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    copy_button.configure(state=NORMAL)

# Copy password to clipboard
def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Password Manager", "Password copied to clipboard!")
    else:
        messagebox.showerror("Password Manager", "No password generated!")

# Save password to database
def save_password():
    password = password_entry.get()

    if password:
        conn = sqlite3.connect("passwords.db")
        c = conn.cursor()
        c.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Password Manager", "Password saved successfully!")
    else:
        messagebox.showerror("Password Manager", "Please generate a password first!")

# Toggle password visibility
def toggle_password_visibility():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_visibility_button.config(text="🔓")  # Set unlock symbol
    else:
        password_entry.config(show="*")
        toggle_visibility_button.config(text="🔐")  # Set lock symbol

# Create GUI window
window = Tk()
window.title("Password Manager")
window.geometry("600x400")

# Create lock emoji label
lock_label = Label(window, text="🔒", font=("Arial", 60))
lock_label.pack(pady=20)

# Create entry field
password_entry = Entry(window, show="*", width=30)
password_entry.pack(pady=10)

# Create options frame
options_frame = ttk.Frame(window)
options_frame.pack(pady=10)

# Password Length Label and Entry
password_length_label = Label(options_frame, text="Password Length:")
password_length_label.grid(row=0, column=0, padx=5, pady=5)
password_length_var = IntVar()
password_length_var.set(12)  # Default password length
password_length_entry = Spinbox(options_frame, from_=8, to=32, textvariable=password_length_var)
password_length_entry.grid(row=0, column=1, padx=5, pady=5)

# Checkbox options for password generation
include_uppercase_var = BooleanVar()
include_uppercase_var.set(True)
include_uppercase_checkbox = Checkbutton(options_frame, text="Include Uppercase", variable=include_uppercase_var)
include_uppercase_checkbox.grid(row=1, column=0, padx=5, pady=5)

include_lowercase_var = BooleanVar()
include_lowercase_var.set(True)
include_lowercase_checkbox = Checkbutton(options_frame, text="Include Lowercase", variable=include_lowercase_var)
include_lowercase_checkbox.grid(row=1, column=1, padx=5, pady=5)

include_digits_var = BooleanVar()
include_digits_var.set(True)
include_digits_checkbox = Checkbutton(options_frame, text="Include Digits", variable=include_digits_var)
include_digits_checkbox.grid(row=2, column=0, padx=5, pady=5)

include_special_chars_var = BooleanVar()
include_special_chars_var.set(False)
include_special_chars_checkbox = Checkbutton(options_frame, text="Include Special Characters", variable=include_special_chars_var)
include_special_chars_checkbox.grid(row=2, column=1, padx=5, pady=5)

# Eye icon for password visibility toggle
toggle_visibility_button = ttk.Button(window, text="🔐", command=toggle_password_visibility)
toggle_visibility_button.pack(pady=5)

# Create buttons
generate_button = ttk.Button(window, text="Generate Password", command=generate_password)
generate_button.pack(pady=5)

copy_button = ttk.Button(window, text="Copy Password", command=copy_password, state=DISABLED)
copy_button.pack(pady=5)

save_button = ttk.Button(window, text="Save Password", command=save_password)
save_button.pack(pady=5)

# Create a database table for passwords if it doesn't exist
conn = sqlite3.connect("passwords.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, password TEXT)")
conn.commit()
conn.close()

# Run the GUI window
window.mainloop()
