# import sqlite3
# from datetime import datetime
# from random import randint
# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# # Replace the last two digits of the column values with "2023"
# # cursor.execute("UPDATE attendance SET date = SUBSTR(date, 1, LENGTH(date) - 2) || '2023' WHERE date LIKE '%23'")
# # cursor.execute("ALTER TABLE attendance ADD COLUMN month VARCHAR(20) DEFAULT 'January'")
# # Define the values for the rows
# id_values = range(1, 11)  # id from 1 to 10
# date_value = "31-01-2023"  # date as a string
# status_values = [randint(0, 1) for _ in range(10)]  # random status values (0 or 1)

# # Insert the rows into the table
# for id, status in zip(id_values, status_values):
#     cursor.execute(
#         "INSERT INTO attendance (id, date, status) VALUES (?, ?, ?)",
#         (id, date_value, status),
#     )
# conn.commit()
# conn.close()


import sqlite3

def create_tasks_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    due TEXT,
                    status TEXT
                )''')

    conn.commit()
    conn.close()

def insert_tasks():
    tasks = [
        {
            "name": "Complete assignment",
            "due": "2023-06-20",
            "status": "In progress"
        },
        {
            "name": "Study for exam",
            "due": "2023-06-25",
            "status": "Not started"
        },
        {
            "name": "Submit project report",
            "due": "2023-06-30",
            "status": "Completed"
        }
    ]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    for task in tasks:
        c.execute("INSERT INTO tasks (name, due, status) VALUES (?, ?, ?)",
                  (task["name"], task["due"], task["status"]))

    conn.commit()
    conn.close()

# Call the functions to create the table and insert the tasks
create_tasks_table()
insert_tasks()
