import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='webgui'
    )

# Function to add student to the database
def add_student():
    studentname = e2.get()
    coursename = e3.get()
    fee = e4.get()

    if not studentname or not coursename or not fee:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO registration (name, course, fee) VALUES (%s, %s, %s)"
        values = (studentname, coursename, fee)

        cursor.execute(sql, values)
        conn.commit()

        messagebox.showinfo("Success", "✅ Student record added successfully!")

        clear_fields()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert student: {err}")
    finally:
        conn.close()

# Function to update student record
def update_student():
    selected_item = listBox.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to update.")
        return

    studentid = e1.get()
    studentname = e2.get()
    coursename = e3.get()
    fee = e4.get()

    if not studentname or not coursename or not fee:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE registration SET name=%s, course=%s, fee=%s WHERE id=%s"
        values = (studentname, coursename, fee, studentid)

        cursor.execute(sql, values)
        conn.commit()

        messagebox.showinfo("Success", "✅ Student record updated successfully!")

        clear_fields()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to update student: {err}")
    finally:
        conn.close()

# Function to delete a student
def delete_student():
    studentid = e1.get()

    if not studentid:
        messagebox.showerror("Selection Error", "Please select a student to delete.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM registration WHERE id=%s"
        cursor.execute(sql, (studentid,))
        conn.commit()

        messagebox.showinfo("Success", "✅ Student record deleted successfully!")

        clear_fields()
        load_students()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to delete student: {err}")
    finally:
        conn.close()

# Function to load students into the Treeview
def load_students():
    for row in listBox.get_children():
        listBox.delete(row)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM registration")
        rows = cursor.fetchall()

        for row in rows:
            listBox.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to load students: {err}")
    finally:
        conn.close()

# Function to populate the entry fields when a row is selected
def on_treeview_select(event):
    selected_item = listBox.selection()
    if selected_item:
        student = listBox.item(selected_item)
        studentid, studentname, coursename, fee = student['values']

        e1.config(state="normal")
        e1.delete(0, tk.END)
        e1.insert(0, studentid)

        e2.delete(0, tk.END)
        e2.insert(0, studentname)

        e3.delete(0, tk.END)
        e3.insert(0, coursename)

        e4.delete(0, tk.END)
        e4.insert(0, fee)

# Function to clear all entry fields
def clear_fields():
    e1.config(state="normal")
    e1.delete(0, tk.END)
    e1.config(state="disabled")
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)

# Function to search students by name
def search_student():
    query = search_var.get().lower()
    for row in listBox.get_children():
        listBox.delete(row)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM registration WHERE LOWER(name) LIKE %s", (f"%{query}%",))
        rows = cursor.fetchall()

        for row in rows:
            listBox.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to search students: {err}")
    finally:
        conn.close()

# Create the main window
root = tk.Tk()
root.geometry('700x600')
root.title("Student Registration System")

# Load and display the header image
try:
    image = Image.open("logo.png")
    image = image.resize((700, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    header = tk.Label(root, image=photo)
    header.image = photo
    header.pack()
except Exception as e:
    print(f"Error loading image: {e}")

# Apply styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TLabel", font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

# Create frames
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(fill="x")

button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill="x")

search_frame = ttk.Frame(root, padding="10")
search_frame.pack(fill="x")

tree_frame = ttk.Frame(root, padding="10")
tree_frame.pack(fill="both", expand=True)

# Labels and Entry Fields
ttk.Label(form_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Label(form_frame, text="Name").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Label(form_frame, text="Course").grid(row=2, column=0, padx=5, pady=5, sticky="e")
ttk.Label(form_frame, text="Fee").grid(row=3, column=0, padx=5, pady=5, sticky="e")

e1 = ttk.Entry(form_frame)
e1.grid(row=0, column=1, padx=5, pady=5)
e1.config(state="disabled")

e2 = ttk.Entry(form_frame)
e2.grid(row=1, column=1, padx=5, pady=5)

e3 = ttk.Entry(form_frame)
e3.grid(row=2, column=1, padx=5, pady=5)

e4 = ttk.Entry(form_frame)
e4.grid(row=3, column=1, padx=5, pady=5)

# Buttons
ttk.Button(button_frame, text="Add", command=add_student).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Update", command=update_student).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Delete", command=delete_student).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Clear", command=clear_fields).grid(row=0, column=3, padx=5, pady=5)

# Search functionality
search_var = tk.StringVar()
ttk.Label(search_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(search_frame, text="Search", command=search_student).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(search_frame, text="Show All", command=load_students).grid(row=0, column=3, padx=5, pady=5)

# Treeview to display students
cols = ("id", "name", "course", "fee")
listBox = ttk.Treeview(tree_frame, columns=cols, show="headings")
listBox.pack(fill="both", expand=True)

for col in cols:
    listBox.heading(col, text=col.capitalize())
    listBox.column(col, width=150)

# Bind the select event to populate entry fields when a row is clicked
listBox.bind("<ButtonRelease-1>", on_treeview_select)

# Load the student records when the application starts
load_students()

# Start the Tkinter event loop
root.mainloop()
