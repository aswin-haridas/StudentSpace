from flask import Flask, render_template
import sqlite3

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
