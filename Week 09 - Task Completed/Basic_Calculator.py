import tkinter as tk

def calculate(operation):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        if operation == "add":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mul":
            result = num1 * num2
        elif operation == "div":
            result = num1 / num2

        result_label.config(text=f"Result: {result}")

    except Exception as e:
        result_label.config(text="Error")

# Main Window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x300")

#Widgets

# Inputs
tk.Label(root, text="Enter first number").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter second number").pack()
entry2 = tk.Entry(root)
entry2.pack()

# Buttons
tk.Button(root, text="Add", command=lambda: calculate("add")).pack(pady=5)
tk.Button(root, text="Subtract", command=lambda: calculate("sub")).pack(pady=5)
tk.Button(root, text="Multiply", command=lambda: calculate("mul")).pack(pady=5)
tk.Button(root, text="Divide", command=lambda: calculate("div")).pack(pady=5)

# Result
result_label = tk.Label(root, text="Result: ")
result_label.pack(pady=10)

root.mainloop()