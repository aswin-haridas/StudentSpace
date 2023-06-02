from flask import Flask, render_template, request, redirect, url_for
from openpyxl import load_workbook
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    admin = "/static/assets/admin.png"
    student = "/static/assets/student.png"
    faculty = "/static/assets/faculty.png"

    if request.method == "POST":
        user_type = request.form.get("user-type")
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM studentlist WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is not None:
            name = result[0]
            if user_type == "student":
                return redirect(url_for("student_home", name=name))
            elif user_type == "faculty":
                return redirect(url_for("faculty_home", name=name))
            elif user_type == "admin":
                return redirect(url_for("admin_home", name=name))
        error_message = "Invalid username or password"
        return render_template("login.html", error=error_message)
    return render_template("login.html", admin=admin, faculty=faculty, student=student)

@app.route("/home/<name>", endpoint="student_home")
def student_home(name):
    return render_template("home-student.html", name=name)

@app.route("/home/<name>", endpoint="faculty_home")
def faculty_home(name):
    return render_template("home-faculty.html", name=name)

@app.route("/home/<name>", endpoint="admin_home")
def admin_home(name):
    return render_template("home-admin.html", name=name)

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    wb = load_workbook(file)
    sheet = wb.active
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            date,
            student_id,
            attendance_status
        )
    """)
    for row in sheet.iter_rows(min_row=2):
        date, student_id, attendance_status = row
        cursor.execute("INSERT INTO attendance VALUES (?, ?, ?)", (date, student_id, attendance_status))
    conn.commit()
    conn.close()
    message = "File uploaded successfully!"
    return render_template("upload.html", message=message)

@app.route("/attendance")
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM attendance WHERE date = ?"
    date = "01/01/2022"
    cursor.execute(query, (date,))
    attendance_data = cursor.fetchall()
    conn.close()
    return render_template("attendance.html", attendance=attendance_data)

@app.route('/courses')
def courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()

    return render_template('courses.html', courses=courses)


if __name__ == "__main__":
    app.run(debug=True)
