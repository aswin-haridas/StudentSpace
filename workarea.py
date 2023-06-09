import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Retrieve the date from the database
cursor.execute("SELECT date FROM attendance")
rows = cursor.fetchall()

# Iterate over the retrieved rows and update the date format
for row in rows:
    old_date_str = row[0]
    old_date = datetime.strptime(old_date_str, "%Y-%m-%d %H:%M:%S")
    new_date_str = old_date.strftime("%d-%m-%y")
    
    # Update the date in the database
    cursor.execute("UPDATE attendance SET date = ? WHERE date = ?", (new_date_str, old_date_str))

# Commit the changes and close the connection
conn.commit()
conn.close()
