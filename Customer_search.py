import tkinter as tk
from tkinter import ttk, PhotoImage
import mysql.connector

def get_db_connection():
    # Create and return database connection and cursor
    conn = mysql.connector.connect(host='', user='', password='', db='')
    cursor = conn.cursor()
    return conn, cursor

def load_customers():
    # Clear existing data in the treeview
    for i in tree.get_children():
        tree.delete(i)

    # Database connection
    conn, cursor = get_db_connection()

    # SQL query to fetch specific fields from customer and address tables
    cursor.execute("""
          SELECT 
              customer.first_name,
              customer.last_name,
              customer.email,
              customer.active,
              customer.create_date,
              address.address,
              address.district,
              address.postal_code,
              address.phone
          FROM customer
          JOIN address ON customer.id = address.customer_id
      """)

    # Inserting data into the treeview
    for row in cursor:
        tree.insert('', 'end', values=row)

    cursor.close()
    conn.close()

def search_customers(*args):
    # Fetch input from textboxes
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    # Database connection
    conn, cursor = get_db_connection()

    # SQL query with filters

    query = """
        SELECT
            c.first_name,
            c.last_name,
            c.email,
            c.active,
            c.create_date,
            o.address,
            o.district,
            o.postal_code,
            o.phone
        FROM
            customer c
        LEFT JOIN
            address o ON c.id = o.customer_id
        WHERE
            c.first_name LIKE %s
            AND c.last_name LIKE %s
    """
    cursor.execute(query, ('%' + first_name + '%', '%' + last_name + '%'))

    # Update the treeview with the search results
    for i in tree.get_children():
        tree.delete(i)

    for row in cursor:
        tree.insert('', 'end', values=row)

    cursor.close()
    conn.close()

# GUI setup
root = tk.Tk()
root.title("Sakila Customer Info")

# Load and set the window icon
icon = PhotoImage(file="valley.png")  # Replace with the path to your icon
root.iconphoto(False, icon)

# Entry widgets for first name and last name
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=0, column=0)
first_name_entry.bind("<KeyRelease>", search_customers)  # Bind KeyRelease event to search_customers

last_name_entry = tk.Entry(root)
last_name_entry.grid(row=1, column=0)
last_name_entry.bind("<KeyRelease>", search_customers)  # Bind KeyRelease event to search_customers

# Labels positioned to the left of the textboxes
tk.Label(root, text="First Name:").grid(row=0, column=0, sticky='w', padx=440)
tk.Label(root, text="Last Name:").grid(row=1, column=0, sticky='w', padx=440)

# Configure style for Treeview
style = ttk.Style()
style.configure("Treeview", background="white", fieldbackground="white", foreground="blue")
style.configure("Treeview.Heading", foreground="blue", background="silver")  # Optional: style for headings
style.configure("Treeview", rowheight=25)  # Increase row height for better visibility
style.configure("Treeview", borderwidth=25, relief="raised")  # Increase border width of cells (mimicking grid lines)

# Treeview widget for displaying results
columns = ("first_name", "last_name", "email", "active", "create_date", "address_id", "district", "postcode",
          "phone")
tree = ttk.Treeview(root, columns=columns, show='headings', style='Treeview')
# Set column headings and widths

tree.column("first_name", width=150)
tree.column("last_name", width=150)
tree.column("email", width=300)
tree.column("active", width=60)
tree.column("create_date", width=150)
tree.column("address_id", width=70)
tree.column("district", width=150)
tree.column("postcode", width=150)
tree.column("phone", width=150)

for col in columns:
    tree.heading(col, text=col.title())

# Scrollbars
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Grid layout for treeview and scrollbars
tree.grid(row=3, column=0, sticky='nsew')
vsb.grid(row=3, column=1, sticky='ns')
hsb.grid(row=4, column=0, sticky='ew')

# Load all customers initially
load_customers()

root.mainloop()
