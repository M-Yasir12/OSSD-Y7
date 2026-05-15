import tkinter as tk
from tkinter import messagebox
# Simple Student Manager Application using Tkinter

#main window
root = tk.Tk()
root.title("Student Manager")
root.geometry("400x400")

# Input
tk.Label(root, text="Enter Student Name").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Add Student
def add_student():
    name = entry.get()

    if name == "":
        messagebox.showwarning("Input Error", "Name cannot be empty!")
        return

    try:
        with open("students.txt", "a") as file:
            file.write(name + "\n")

        messagebox.showinfo("Success", "Student added successfully!")
        entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# View Students
def view_students():
    try:
        with open("students.txt", "r") as file:
            data = file.read()

        if data == "":
            messagebox.showinfo("Students", "No students found!")
        else:
            messagebox.showinfo("Student List", data)

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

# Buttons
tk.Button(root, text="Add Student", command=add_student).pack(pady=10)
tk.Button(root, text="View Students", command=view_students).pack(pady=10)

root.mainloop()