# Author: Daham Dissanayake (Updated version with GUI)
# Date: 20/04/2025
# Use: Personal Task Manager GUI with Tkinter


import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Define the Task class to represent each task
class Task:
    def __init__(self, name, description, priority, due_date):
        # Initialize task properties
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        # Convert task properties to a dictionary for JSON serialization
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }
    
    @classmethod
    def from_dict(cls, task_dict):
        # Create a Task object from a dictionary
        return cls(
            task_dict["name"],
            task_dict["description"],
            task_dict["priority"],
            task_dict["due_date"]
        )

# Define the TaskManager class to handle task operations
class TaskManager:
    def __init__(self, json_file='tasks.json'):
        # Initialize TaskManager with a list of tasks and load tasks from JSON
        self.json_file = json_file
        self.tasks = []
        self.load_tasks_from_json()

    def load_tasks_from_json(self):
        # Load tasks from a JSON file into the task list
        try:
            with open(self.json_file, "r") as file:
                task_dicts = json.load(file)
                self.tasks = [Task.from_dict(task_dict) for task_dict in task_dicts]
            print(f"Loaded {len(self.tasks)} tasks from {self.json_file}")
        except FileNotFoundError:
            print(f"File {self.json_file} not found. Starting with empty task list.")
            self.tasks = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.json_file}. Starting with empty task list.")
            self.tasks = []

    def save_tasks_to_json(self):
        # Save tasks to JSON file
        with open(self.json_file, "w") as file:
            task_dicts = [task.to_dict() for task in self.tasks]
            json.dump(task_dicts, file, indent=2)
        print(f"Tasks saved to {self.json_file}")

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        # Return tasks filtered by name, priority, or due date
        filtered_tasks = self.tasks.copy()
        
        if name_filter and name_filter.strip():
            filtered_tasks = [task for task in filtered_tasks if name_filter.lower() in task.name.lower()]
        
        if priority_filter and priority_filter.strip() and priority_filter.lower() != "all":
            filtered_tasks = [task for task in filtered_tasks if task.priority.lower() == priority_filter.lower()]
        
        if due_date_filter and due_date_filter.strip():
            filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date_filter]
        
        return filtered_tasks

    def sort_tasks(self, sort_key='name', reverse=False):
        # Sort tasks by the specified key (e.g., name, priority, due date)
        if sort_key == 'name':
            self.tasks.sort(key=lambda task: task.name.lower(), reverse=reverse)
        elif sort_key == 'priority':
            # Custom sort order for priority: high, medium, low
            priority_order = {"high": 0, "medium": 1, "low": 2}
            self.tasks.sort(key=lambda task: priority_order.get(task.priority.lower(), 3), reverse=reverse)
        elif sort_key == 'due_date':
            self.tasks.sort(key=lambda task: datetime.strptime(task.due_date, "%Y-%m-%d"), reverse=reverse)
        return self.tasks

    def add_task(self, name, description, priority, due_date):
        # Add a new task
        task = Task(name, description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks_to_json()
        return task
    
    def update_task(self, index, name, description, priority, due_date):
        # Update an existing task
        if 0 <= index < len(self.tasks):
            self.tasks[index] = Task(name, description, priority, due_date)
            self.save_tasks_to_json()
            return True
        return False
    
    def delete_task(self, index):
        # Delete a task
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks_to_json()
            return True
        return False

# Define the TaskManagerGUI class to create the Tkinter interface
class TaskManagerGUI:
    def __init__(self, root):
        # Initialize GUI components and set up the Tkinter window
        self.root = root
        self.root.title("Personal Task Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.task_manager = TaskManager()
        self.setup_gui()
        self.populate_tree()
        
        # Track the current sort column and order
        self.sort_column = "name"
        self.sort_reverse = False

    def setup_gui(self):
        # Create and place GUI components (labels, entry fields, buttons, table)
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Personal Task Manager", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # Search and Filter Section
        filter_frame = ttk.LabelFrame(main_frame, text="Search and Filter")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Filter by name
        name_frame = ttk.Frame(filter_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        name_label = ttk.Label(name_frame, text="Filter by Name:")
        name_label.pack(side=tk.LEFT, padx=5)
        self.name_filter = ttk.Entry(name_frame, width=30)
        self.name_filter.pack(side=tk.LEFT, padx=5)
        
        # Filter by priority
        priority_frame = ttk.Frame(filter_frame)
        priority_frame.pack(fill=tk.X, padx=5, pady=5)
        priority_label = ttk.Label(priority_frame, text="Filter by Priority:")
        priority_label.pack(side=tk.LEFT, padx=5)
        self.priority_filter = ttk.Combobox(priority_frame, width=10, values=["All", "High", "Medium", "Low"])
        self.priority_filter.current(0)
        self.priority_filter.pack(side=tk.LEFT, padx=5)
        
        # Filter by due date
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        date_label = ttk.Label(date_frame, text="Filter by Due Date (YYYY-MM-DD):")
        date_label.pack(side=tk.LEFT, padx=5)
        self.date_filter = ttk.Entry(date_frame, width=15)
        self.date_filter.pack(side=tk.LEFT, padx=5)
        
        # Filter button
        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=self.apply_filter)
        filter_button.pack(padx=5, pady=5)
        
        # Reset filters button
        reset_button = ttk.Button(filter_frame, text="Reset Filters", command=self.reset_filters)
        reset_button.pack(padx=5, pady=5)
        
        # Task table frame
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create Treeview
        columns = ("name", "description", "priority", "due_date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define column headings
        self.tree.heading("name", text="Name", command=lambda: self.on_column_click("name"))
        self.tree.heading("description", text="Description", command=lambda: self.on_column_click("description"))
        self.tree.heading("priority", text="Priority", command=lambda: self.on_column_click("priority"))
        self.tree.heading("due_date", text="Due Date", command=lambda: self.on_column_click("due_date"))
        
        # Define column widths
        self.tree.column("name", width=150, anchor=tk.W)
        self.tree.column("description", width=300, anchor=tk.W)
        self.tree.column("priority", width=100, anchor=tk.CENTER)
        self.tree.column("due_date", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Sort buttons
        sort_frame = ttk.Frame(main_frame)
        sort_frame.pack(fill=tk.X, padx=5, pady=5)
        
        sort_label = ttk.Label(sort_frame, text="Sort by:")
        sort_label.pack(side=tk.LEFT, padx=5)
        
        sort_name_btn = ttk.Button(sort_frame, text="Name", 
                                   command=lambda: self.sort_tasks("name"))
        sort_name_btn.pack(side=tk.LEFT, padx=5)
        
        sort_priority_btn = ttk.Button(sort_frame, text="Priority", 
                                      command=lambda: self.sort_tasks("priority"))
        sort_priority_btn.pack(side=tk.LEFT, padx=5)
        
        sort_date_btn = ttk.Button(sort_frame, text="Due Date", 
                                  command=lambda: self.sort_tasks("due_date"))
        sort_date_btn.pack(side=tk.LEFT, padx=5)
        
        # Task management buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = ttk.Button(button_frame, text="Add New Task", command=self.add_task_dialog)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(button_frame, text="Edit Task", command=self.edit_task_dialog)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)

    def populate_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get current filters
        name_filter = self.name_filter.get()
        priority_filter = self.priority_filter.get()
        date_filter = self.date_filter.get()
        
        # Get filtered tasks
        filtered_tasks = self.task_manager.get_filtered_tasks(name_filter, priority_filter, date_filter)
        
        # Insert tasks into the treeview
        for task in filtered_tasks:
            self.tree.insert("", tk.END, values=(task.name, task.description, task.priority, task.due_date))
    
    def apply_filter(self):
        # Apply filter criteria based on user input and refresh the task display
        self.populate_tree()
    
    def reset_filters(self):
        # Reset all filters to their default values
        self.name_filter.delete(0, tk.END)
        self.priority_filter.current(0)  # Reset to "All"
        self.date_filter.delete(0, tk.END)
        self.populate_tree()
    
    def on_column_click(self, column):
        # Toggle sorting order when a column is clicked
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        self.sort_tasks(column)
    
    def sort_tasks(self, sort_key):
        # Sort tasks by a specific column and update the task display
        self.sort_column = sort_key
        self.task_manager.sort_tasks(sort_key, self.sort_reverse)
        self.populate_tree()
    
    def add_task_dialog(self):
        # Open a dialog to add a new task
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Task")
        add_window.geometry("400x300")
        add_window.resizable(False, False)
        add_window.transient(self.root)  # Set to be on top of the main window
        
        # Create form fields
        ttk.Label(add_window, text="Task Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(add_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(add_window, width=30)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(add_window, text="Priority:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        priority_combo = ttk.Combobox(add_window, width=10, values=["High", "Medium", "Low"])
        priority_combo.current(1)  # Default to "Medium"
        priority_combo.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(add_window, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        date_entry = ttk.Entry(add_window, width=15)
        date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Function to validate and add the task
        def add_task():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            priority = priority_combo.get()
            due_date = date_entry.get().strip()
            
            # Simple validation
            if not name:
                messagebox.showerror("Error", "Task name cannot be empty")
                return
            
            if not self.validate_date(due_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Add the task
            self.task_manager.add_task(name, description, priority.lower(), due_date)
            add_window.destroy()
            self.populate_tree()
        
        # Add and Cancel buttons
        ttk.Button(add_window, text="Add Task", command=add_task).grid(row=4, column=0, padx=10, pady=20)
        ttk.Button(add_window, text="Cancel", command=add_window.destroy).grid(row=4, column=1, padx=10, pady=20)
    
    def edit_task_dialog(self):
        # Open a dialog to edit the selected task
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a task to edit")
            return
        
        # Get the index of the selected task
        item_id = selected_item[0]
        item_values = self.tree.item(item_id, "values")
        item_name = item_values[0]
        
        # Find the task index in the task_manager's list
        task_index = -1
        for i, task in enumerate(self.task_manager.tasks):
            if task.name == item_name:
                task_index = i
                break
        
        if task_index == -1:
            messagebox.showerror("Error", "Task not found")
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x300")
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        
        # Get the task
        task = self.task_manager.tasks[task_index]
        
        # Create form fields
        ttk.Label(edit_window, text="Task Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.insert(0, task.name)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(edit_window, width=30)
        desc_entry.insert(0, task.description)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Priority:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        priority_combo = ttk.Combobox(edit_window, width=10, values=["High", "Medium", "Low"])
        priority_index = {"high": 0, "medium": 1, "low": 2}.get(task.priority.lower(), 1)
        priority_combo.current(priority_index)
        priority_combo.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(edit_window, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        date_entry = ttk.Entry(edit_window, width=15)
        date_entry.insert(0, task.due_date)
        date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Function to validate and update the task
        def update_task():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            priority = priority_combo.get()
            due_date = date_entry.get().strip()
            
            # Simple validation
            if not name:
                messagebox.showerror("Error", "Task name cannot be empty")
                return
            
            if not self.validate_date(due_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Update the task
            success = self.task_manager.update_task(task_index, name, description, priority.lower(), due_date)
            if success:
                edit_window.destroy()
                self.populate_tree()
            else:
                messagebox.showerror("Error", "Failed to update task")
        
        # Update and Cancel buttons
        ttk.Button(edit_window, text="Update Task", command=update_task).grid(row=4, column=0, padx=10, pady=20)
        ttk.Button(edit_window, text="Cancel", command=edit_window.destroy).grid(row=4, column=1, padx=10, pady=20)
    
    def delete_task(self):
        # Delete the selected task
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Selection Required", "Please select a task to delete")
            return
        
        # Get the index of the selected task
        item_id = selected_item[0]
        item_values = self.tree.item(item_id, "values")
        item_name = item_values[0]
        
        # Find the task index in the task_manager's list
        task_index = -1
        for i, task in enumerate(self.task_manager.tasks):
            if task.name == item_name:
                task_index = i
                break
        
        if task_index == -1:
            messagebox.showerror("Error", "Task not found")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task '{item_name}'?")
        if confirm:
            success = self.task_manager.delete_task(task_index)
            if success:
                self.populate_tree()
            else:
                messagebox.showerror("Error", "Failed to delete task")
    
    def validate_date(self, date):
        try:
            # Check format YYYY-MM-DD
            if len(date) != 10 or date[4] != '-' or date[7] != '-':
                return False
            
            # Extract year, month, day
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            
            # Basic validation
            if year < 1900 or year > 2100:
                return False
            if month < 1 or month > 12:
                return False
            
            # Check day based on month
            days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            # Adjust February for leap years
            if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
                days_in_month[2] = 29
                
            if day < 1 or day > days_in_month[month]:
                return False
            return True
        except (ValueError, IndexError):
            return False

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()