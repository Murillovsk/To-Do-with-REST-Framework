import tkinter as tk
from tkinter import messagebox
import requests


API_URL = "http://127.0.0.1:8000/api/todos/"


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.create_widgets()
        self.fetch_todos()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Title")
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add To-Do", command=self.add_todo)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.todo_listbox = tk.Listbox(
            self.root, selectmode=tk.SINGLE, width=50, height=15
        )
        self.todo_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.complete_button = tk.Button(
            self.root, text="Complete", command=self.complete_todo
        )
        self.complete_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(
            self.root, text="Delete", command=self.delete_todo
        )
        self.delete_button.grid(row=2, column=2, padx=10, pady=10)

    def fetch_todos(self):
        self.todo_listbox.delete(0, tk.END)
        response = requests.get(API_URL)
        if response.status_code == 200:
            todos = response.json()
            self.todos = {todo['id']: todo for todo in todos}
            for todo in todos:
                self.todo_listbox.insert(tk.END, self.format_todo_text(todo))
        else:
            messagebox.showerror("Error", "Failed to fetch to-dos")

    def format_todo_text(self, todo):
        return f"{todo['id']}: {'[X]' if todo['completed'] else '[ ]'} {todo['title']}"

    def add_todo(self):
        title = self.title_entry.get().strip()  # Corrigido para '=' ao invés de '-'
        if title:
            response = requests.post(API_URL, json={"title": title})
            if response.status_code == 201:
                self.fetch_todos()
                self.title_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add to-do")
        else:
            messagebox.showwarning("Input Error", "Title cannot be empty")

    def complete_todo(self):
        selected = self.todo_listbox.curselection()  # Corrigido ',' para '.'
        if selected:
            todo_id = int(self.todo_listbox.get(selected).split(":")[0])
            todo = self.todos[todo_id]
            response = requests.patch(f"{API_URL}{todo_id}/", json={"completed": not todo['completed']})
            if response.status_code == 200:
                self.fetch_todos()
            else:
                messagebox.showerror("Error", "Failed to update to-do")
        else:
            messagebox.showwarning("Selection Error", "No to-do selected")

    def delete_todo(self):
        selected = self.todo_listbox.curselection()
        if selected:
            todo_id = int(self.todo_listbox.get(selected).split(":")[0])
            response = requests.delete(f"{API_URL}{todo_id}/")
            if response.status_code == 204:
                self.fetch_todos()
            else:
                messagebox.showerror("Error", "Failed to delete to-do")
        else:
            messagebox.showwarning("Selection Error", "No to-do selected")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
