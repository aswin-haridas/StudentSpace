import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Modify the schema to include the auto-incrementing primary key column
cursor.execute('''
    CREATE TABLE tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        due_date TEXT,
        status TEXT
    );
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
