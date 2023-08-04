import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        due_date TEXT,
        status TEXT
    );
''')

# Add some example tasks to the table
tasks = [
    ('DBMS assignment 1', '2023-08-10', 'Pending'),
    ('Finish project', '2023-08-15', 'In Progress'),
    ('DS assignment', '2023-08-20', 'Pending'),
]

for task in tasks:
    cursor.execute('INSERT INTO tasks (task_name, due_date, status) VALUES (?, ?, ?)', task)

# Commit the changes and close the connection
conn.commit()
conn.close()
