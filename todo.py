import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import Calendar
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.configure(bg="#FFFFFF")

        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.create_widgets()

        self.update_date_time()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                date TEXT,
                priority TEXT
            )
            """
        )
        self.conn.commit()

    def create_widgets(self):
        self.task_label = tk.Label(self.root, text="Task:", bg="#FFFFFF", fg="#000000")
        self.task_label.grid(row=0, column=0, padx=10, pady=5)

        self.task_entry = tk.Entry(self.root, bg="#FFFFFF", fg="#000000")
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        self.date_label = tk.Label(self.root, text="Date:", bg="#FFFFFF", fg="#000000")
        self.date_label.grid(row=1, column=0, padx=10, pady=5)

        self.calendar_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.calendar_frame.grid(row=1, column=1, padx=10, pady=5)

        self.calendar = Calendar(self.calendar_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month)
        self.calendar.pack()

        self.priority_label = tk.Label(self.root, text="Priority:", bg="#FFFFFF", fg="#000000")
        self.priority_label.grid(row=2, column=0, padx=10, pady=5)

        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set("High")
        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, "High", "Mid", "Low")
        self.priority_menu.configure(bg="#00FFFF", fg="#000000")
        self.priority_menu.grid(row=2, column=1, padx=10, pady=5)

        # Buttons Frame
        self.button_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, bg="#00FFFF", fg="#000000", padx=10)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_selected_task, bg="#00FFFF", fg="#000000", padx=10)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All", command=self.clear_all_tasks, bg="#00FFFF", fg="#000000", padx=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit_application, bg="#00FFFF", fg="#000000", padx=10)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Treeview widget with separate columns for task, priority, and date
        self.task_listbox = ttk.Treeview(self.root, columns=("Task", "Priority", "Date"), show="headings", selectmode="browse")
        self.task_listbox.heading("Task", text="Task")
        self.task_listbox.heading("Priority", text="Priority")
        self.task_listbox.heading("Date", text="Date")
        self.task_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.task_listbox.bind("<ButtonRelease-1>", self.select_task)  # Bind click event to select_task method

        self.date_time_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#FFFFFF", fg="#999999")
        self.date_time_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.load_tasks()

    def load_tasks(self):
        # Clear existing rows in the task_listbox
        for row in self.task_listbox.get_children():
            self.task_listbox.delete(row)

        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.task_listbox.insert("", tk.END, values=(task[1], task[3], task[2]))

    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.calendar.selection_get().strftime("%Y-%m-%d")
        priority = self.priority_var.get()

        if task:
            self.cursor.execute("INSERT INTO tasks (task, date, priority) VALUES (?, ?, ?)", (task, date, priority))
            self.conn.commit()
            self.load_tasks()
            self.task_entry.delete(0, tk.END)
            self.calendar.set_date(datetime.now())
            self.priority_var.set("High")
        else:
            messagebox.showerror("Error", "Please enter a task.")

    def select_task(self, event):
        # Get the selected item's task_id from the treeview
        selected_item = self.task_listbox.selection()
        if selected_item:
            self.selected_task_id = self.task_listbox.item(selected_item, "values")[0]
        else:
            self.selected_task_id = None

    def delete_selected_task(self):
        if self.selected_task_id:
            response = messagebox.askyesno("Delete Task", "Are you sure you want to delete the selected task?")
            if response == tk.YES:
                self.cursor.execute("DELETE FROM tasks WHERE id=?", (self.selected_task_id,))
                self.conn.commit()
                self.load_tasks()
        else:
            messagebox.showerror("Error", "Please select a task to delete.")

    def clear_all_tasks(self):
        response = messagebox.askyesno("Clear All Tasks", "Are you sure you want to clear all tasks?")
        if response == tk.YES:
            self.cursor.execute("DELETE FROM tasks")
            self.conn.commit()
            self.load_tasks()

    def quit_application(self):
        self.conn.close()
        self.root.quit()

    def update_date_time(self):
        now = datetime.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=current_date_time)
        self.root.after(1000, self.update_date_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
