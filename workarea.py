import pandas as pd
import sqlite3

# Read the Excel file
df = pd.read_excel('accounts.xlsx')  # Replace 'usernames.xlsx' with your actual file name

# Establish a connection to the SQLite database
conn = sqlite3.connect('database.db')  # Replace 'database.db' with your database file name
cursor = conn.cursor()

# Create a table to store the usernames and passwords
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
''')

# Iterate over the rows of the DataFrame and insert data into the database
for _, row in df.iterrows():
    username = row['USERNAME']
    password = row['PASSWORD']
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

# Commit the changes and close the connection
conn.commit()
conn.close()
