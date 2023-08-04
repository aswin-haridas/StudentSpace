import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Add a new column named 'pfp' to the 'users' table
cursor.execute("ALTER TABLE facultylist ADD COLUMN pfp TEXT")

# Fetch all rows from the 'users' table
cursor.execute("SELECT id, username FROM users")
rows = cursor.fetchall()

# Update the 'pfp' column for each row
for row in rows:
    user_id, username = row
    new_pfp = username + ".png"
    cursor.execute("UPDATE facultylist SET pfp = ? WHERE id = ?", (new_pfp, user_id))

# Commit the changes
conn.commit()

# Close the connection
conn.close()
