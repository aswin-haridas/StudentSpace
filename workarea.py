import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the "grade" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS grade (
        id INTEGER PRIMARY KEY,
        ip INTEGER,
        ds INTEGER,
        dbms INTEGER,
        algo INTEGER,
        os INTEGER
    )
''')

# Read the CSV file and insert data into the "grade" table
with open('student.csv', 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Skip the header row

    for row in csv_data:
        id, ip, ds, dbms, algo, os = row
        cursor.execute('''
            INSERT INTO grade (id, ip, ds, dbms, algo, os)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, ip, ds, dbms, algo, os))

# Commit the changes and close the connection
conn.commit()
conn.close()
