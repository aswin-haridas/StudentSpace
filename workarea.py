import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create a table called "students"
c.execute('''CREATE TABLE IF NOT EXISTS facultylist
             (id INTEGER, name TEXT, dob TEXT, email TEXT, course TEXT, contact TEXT, address TEXT)''')

# Read the CSV file and insert the data into the table
with open('students.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row

    for row in reader:
        c.execute("INSERT INTO facultylist VALUES (?, ?, ?, ?, ?, ?, ?)", row)

# Commit the changes and close the connection
conn.commit()
conn.close()
