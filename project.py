import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Global variables
connection = None
selected_id = None

# Entry widgets (global variables)
name_entry = None
category_entry = None
quantity_entry = None
price_entry = None
supplier_entry = None
search_entry = None
tree = None

def connect_database():
    global connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='inventory_db',
            user='root',
            password=''  # Default XAMPP password is empty
        )
        if connection.is_connected():
            create_table()
            print("Database connected successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")

def create_table():
    global connection
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                quantity INT DEFAULT 0,
                price DECIMAL(10,2) DEFAULT 0.00,
                supplier VARCHAR(100)
            )
        """)
        connection.commit()
    except Error as e:
        messagebox.showerror("Database Error", f"Error creating table: {e}")

def validate_inputs():
    if not name_entry.get().strip():
        messagebox.showerror("Input Error", "Product name is required!")
        return False
    
    try:
        int(quantity_entry.get())
        float(price_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for quantity and price!")
        return False
    
    return True

def add_product():
    global connection
    if not validate_inputs():
        return
    
    try:
        cursor = connection.cursor()
        query = """INSERT INTO products (name, category, quantity, price, supplier) 
                  VALUES (%s, %s, %s, %s, %s)"""
        values = (
            name_entry.get(),
            category_entry.get(),
            int(quantity_entry.get()),
            float(price_entry.get()),
            supplier_entry.get()
        )
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        clear_fields()
        load_data()
    except Error as e:
        messagebox.showerror("Database Error", f"Error adding product: {e}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid quantity and price!")

def update_product():
    global connection, selected_id
    if not selected_id:
        messagebox.showwarning("Selection Error", "Please select a product to update!")
        return
    
    if not validate_inputs():
        return
    
    try:
        cursor = connection.cursor()
        query = """UPDATE products SET name=%s, category=%s, quantity=%s, 
                  price=%s, supplier=%s WHERE id=%s"""
        values = (
            name_entry.get(),
            category_entry.get(),
            int(quantity_entry.get()),
            float(price_entry.get()),
            supplier_entry.get(),
            selected_id
        )
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
        clear_fields()
        load_data()
    except Error as e:
        messagebox.showerror("Database Error", f"Error updating product: {e}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid quantity and price!")

def delete_product():
    global connection, selected_id
    if not selected_id:
        messagebox.showwarning("Selection Error", "Please select a product to delete!")
        return
    
    result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
    if result:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (selected_id,))
            connection.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            clear_fields()
            load_data()
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting product: {e}")

def search_product():
    global connection, tree
    search_term = search_entry.get().strip()
    if not search_term:
        messagebox.showwarning("Search Error", "Please enter a search term!")
        return
    
    try:
        cursor = connection.cursor()
        query = """SELECT * FROM products WHERE name LIKE %s OR category LIKE %s 
                  OR supplier LIKE %s"""
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        results = cursor.fetchall()
        
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert search results
        for row in results:
            tree.insert('', 'end', values=row)
    except Error as e:
        messagebox.showerror("Database Error", f"Error searching products: {e}")

def load_data():
    global connection, tree
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id")
        results = cursor.fetchall()
        
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert data
        for row in results:
            tree.insert('', 'end', values=row)
    except Error as e:
        messagebox.showerror("Database Error", f"Error loading data: {e}")

def on_select(event):
    global selected_id, tree
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        values = item['values']
        
        # Store selected ID
        selected_id = values[0]
        
        # Fill entry fields
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        
        category_entry.delete(0, tk.END)
        category_entry.insert(0, values[2])
        
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[3])
        
        price_entry.delete(0, tk.END)
        price_entry.insert(0, values[4])
        
        supplier_entry.delete(0, tk.END)
        supplier_entry.insert(0, values[5])

def clear_fields():
    global selected_id
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    supplier_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    selected_id = None

def create_gui():
    global name_entry, category_entry, quantity_entry, price_entry
    global supplier_entry, search_entry, tree
    
    # Create main window
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("800x600")
    root.configure(bg='#f0f0f0')
    
    # Title
    title_label = tk.Label(root, text="Inventory Management System", 
                          font=('Arial', 16, 'bold'), bg='#f0f0f0')
    title_label.pack(pady=10)
    
    # Input Frame
    input_frame = tk.Frame(root, bg='#f0f0f0')
    input_frame.pack(pady=10, padx=20, fill='x')
    
    # Input fields
    tk.Label(input_frame, text="Product Name:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
    name_entry = tk.Entry(input_frame, width=20)
    name_entry.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(input_frame, text="Category:", bg='#f0f0f0').grid(row=0, column=2, sticky='w', pady=5)
    category_entry = tk.Entry(input_frame, width=15)
    category_entry.grid(row=0, column=3, pady=5, padx=5)
    
    tk.Label(input_frame, text="Quantity:", bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
    quantity_entry = tk.Entry(input_frame, width=20)
    quantity_entry.grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(input_frame, text="Price:", bg='#f0f0f0').grid(row=1, column=2, sticky='w', pady=5)
    price_entry = tk.Entry(input_frame, width=15)
    price_entry.grid(row=1, column=3, pady=5, padx=5)
    
    tk.Label(input_frame, text="Supplier:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
    supplier_entry = tk.Entry(input_frame, width=30)
    supplier_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky='ew')
    
    # Buttons Frame
    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Add Product", command=add_product, 
             bg='#4CAF50', fg='white', width=12).pack(side='left', padx=5)
    tk.Button(button_frame, text="Update Product", command=update_product, 
             bg='#2196F3', fg='white', width=12).pack(side='left', padx=5)
    tk.Button(button_frame, text="Delete Product", command=delete_product, 
             bg='#f44336', fg='white', width=12).pack(side='left', padx=5)
    tk.Button(button_frame, text="Clear Fields", command=clear_fields, 
             bg='#FF9800', fg='white', width=12).pack(side='left', padx=5)
    
    # Search Frame
    search_frame = tk.Frame(root, bg='#f0f0f0')
    search_frame.pack(pady=10)
    
    tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left')
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side='left', padx=5)
    tk.Button(search_frame, text="Search", command=search_product, 
             bg='#9C27B0', fg='white').pack(side='left', padx=5)
    tk.Button(search_frame, text="Show All", command=load_data, 
             bg='#607D8B', fg='white').pack(side='left', padx=5)
    
    # Treeview Frame
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
    
    # Treeview
    columns = ('ID', 'Name', 'Category', 'Quantity', 'Price', 'Supplier')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
    
    # Define headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Bind treeview selection
    tree.bind('<<TreeviewSelect>>', on_select)
    
    return root

def main():
    # Connect to database
    connect_database()
    
    # Create GUI
    root = create_gui()
    
    # Load initial data
    load_data()
    
    # Start the GUI
    root.mainloop()
    
    # Close database connection when done
    if connection and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()