import tkinter as tk
import math
from decimal import Decimal, InvalidOperation

def calculate():
    try:
        expression = entry.get()
        result = str(Decimal(expression))
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except InvalidOperation:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(value))

def clear():
    entry.delete(0, tk.END)

def square_root():
    try:
        expression = entry.get()
        result = str(math.sqrt(Decimal(expression)))
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except InvalidOperation:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def sin():
    try:
        expression = entry.get()
        result = str(math.sin(math.radians(Decimal(expression))))
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except InvalidOperation:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Create the main application window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x500")
root.config(bg="#333")  # Dark background color

# Entry widget to display the result
entry = tk.Entry(root, bg="#444", fg="white", font=("Helvetica", 30))
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Define button labels
button_labels = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+"
]

# Create buttons with black text
row, col = 1, 0
for label in button_labels:
    button = tk.Button(root, text=label, bg="#666", fg="black", font=("Helvetica", 20),
                       command=lambda value=label: button_click(value))
    button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    col += 1
    if col > 3:
        col = 0
        row += 1

# Clear button
clear_button = tk.Button(root, text="C", bg="#999", fg="black", font=("Helvetica", 20), command=clear)
clear_button.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Calculate button
equal_button = tk.Button(root, text="=", bg="#bbb", fg="black", font=("Helvetica", 20), command=calculate)
equal_button.grid(row=row, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

# Square root button
sqrt_button = tk.Button(root, text="√", bg="#999", fg="black", font=("Helvetica", 20), command=square_root)
sqrt_button.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")

# Sin button
sin_button = tk.Button(root, text="sin", bg="#999", fg="black", font=("Helvetica", 20), command=sin)
sin_button.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")

# Configure row and column weights to resize buttons on window resize
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Run the main loop
root.mainloop()
