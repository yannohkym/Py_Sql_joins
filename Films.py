# Designed by _Student Name

import mysql.connector
from tkinter import Tk, ttk, Listbox, N, S, E, W, VERTICAL, Y, RIGHT, X, BOTTOM, HORIZONTAL

# Function to load films based on selected category
def load_films(event):
    selected_category = category_listbox.get(category_listbox.curselection())
    cursor.execute(film_query, (selected_category,))
    films = cursor.fetchall()

    # Clear existing data in treeview
    for item in film_tree.get_children():
        film_tree.delete(item)

    # Insert new data
    for film in films:
        film_tree.insert('', 'end', values=film)

# Connect to the Sakila database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="sakila"
)
cursor = conn.cursor()

# Queries
category_query = "SELECT DISTINCT name FROM category ORDER BY name;"
film_query = """
SELECT f.title, f.description, f.release_year, f.rating, f.special_features, l.name 
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
JOIN language l ON f.language_id = l.language_id
WHERE c.name = %s
ORDER BY f.title;
"""

# GUI setup
root = Tk()
root.title("Sakila Film Browser")

# Create widgets
category_listbox = Listbox(root)
film_tree = ttk.Treeview(root, columns=('Title', 'Description', 'Release Year', 'Rating', 'Special Features', 'Language'))
v_scroll = ttk.Scrollbar(root, orient=VERTICAL, command=film_tree.yview)
h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL, command=film_tree.xview)

# Attach scrollbar to treeview
film_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

# Grid layout
category_listbox.grid(row=0, column=0, sticky=(N, S, E, W))
film_tree.grid(row=0, column=1, sticky=(N, S, E, W))
v_scroll.grid(row=0, column=2, sticky=(N, S))
h_scroll.grid(row=1, column=1, sticky=(E, W))

# Configure columns
film_tree['show'] = 'headings'  # Hide the first empty column
for col in film_tree['columns']:
    film_tree.heading(col, text=col)
    film_tree.column(col, width=100)

# Load categories
cursor.execute(category_query)
for category in cursor:
    category_listbox.insert('end', category[0])

# Bind selection event
category_listbox.bind('<<ListboxSelect>>', load_films)

# Start the GUI
root.mainloop()

# Cleanup
cursor.close()
conn.close()