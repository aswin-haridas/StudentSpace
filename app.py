from flask import Flask, render_template
import sqlite3
from openpyxl import load_workbook

# Open the Excel workbook
wb = load_workbook(filename='data.xlsx')

# Get the active worksheet
ws = wb.active

# Open a connection to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Loop through each row in the worksheet and insert data into the database
for row in ws.iter_rows(min_row=2, values_only=True):
    regbo, name, ADD, CGIP, CD, DA, IEFT = row
    # Insert data into the database
    cursor.execute("INSERT INTO table_name(regno, name, ADD, CGIP, CD, DA, IEFT) VALUES (?, ?, ?, ?, ?, ?, ?)", (regbo, name, ADD, CGIP, CD, DA, IEFT))

app = Flask(__name__,)
@app.route('/')
def show_students():
    # Connect to the database and execute a SELECT query
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()

    # Render the HTML file with the rows of data
    return render_template('perfomance.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
