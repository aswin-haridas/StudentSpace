from flask import Flask, render_template, request ,redirect, url_for
import openpyxl
import sqlite3

app = Flask(__name__)


@app.route("/")
def upload():
    return render_template("upload.html")


@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            date TEXT,
            student_id TEXT,
            attendance_status INTEGER
        )
    """
    )
    for row in sheet.iter_rows(min_row=2):
        date = row[0].value
        student_id = row[1].value
        attendance_status = row[2].value
        cursor.execute(
            "INSERT INTO attendance VALUES (?, ?, ?)",
            (date, student_id, attendance_status),
        )
    conn.commit()
    conn.close()
    message = 'File uploaded successfully!'
    return render_template('upload.html', message=message)


@app.route("/attendance")
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    attendance_data = cursor.fetchall()
    conn.close()
    return render_template("attendance.html", attendance_data=attendance_data)


if __name__ == "__main__":
    app.run(debug=True)
