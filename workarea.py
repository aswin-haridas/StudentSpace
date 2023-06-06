import csv
import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create the studentlist table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS studentlist (
        id INTEGER PRIMARY KEY,
        name TEXT,
        dob TEXT,
        email TEXT,
        course TEXT,
        contact TEXT,
        address TEXT
    )
""")

# Read the CSV file and insert the data into the studentlist table
with open("students.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        id, name, dob, email, course, contact, address = row
        cursor.execute(
            "INSERT INTO studentlist (id, name, dob, email, course, contact, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id, name, dob, email, course, contact, address)
        )

# Commit the changes and close the connection
conn.commit()
conn.close()
