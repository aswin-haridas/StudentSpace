from flask import Flask, render_template, request, redirect, url_for
from openpyxl import load_workbook
import sqlite3

app = Flask(__name__)

import sqlite3


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
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?", (username, password)
        )
        result = cursor.fetchone()
        if result is not None:
            user_id = result[0]
            if user_type == "student":
                cursor.execute(
                    "SELECT firstname, lastname FROM studentlist WHERE id=?", (user_id,)
                )
                user_info = cursor.fetchone()
                if user_info is not None:
                    firstname, lastname = user_info
                    return redirect(
                        url_for(
                            "student_home",
                            username=username,
                            firstname=firstname,
                            lastname=lastname,
                        )
                    )
            elif user_type == "faculty":
                cursor.execute(
                    "SELECT firstname, lastname FROM facultylist WHERE id=?", (user_id,)
                )
                user_info = cursor.fetchone()
                if user_info is not None:
                    firstname, lastname = user_info
                    return redirect(
                        url_for(
                            "faculty_home",
                            username=username,
                            firstname=firstname,
                            lastname=lastname,
                        )
                    )
                pass
            elif user_type == "admin":
                cursor.execute(
                    "SELECT firstname, lastname FROM facultylist WHERE id=?", (user_id,)
                )
                user_info = cursor.fetchone()
                if user_info is not None:
                    firstname, lastname = user_info
                    return redirect(
                        url_for(
                            "admin_home",
                            username=username,
                            firstname=firstname,
                            lastname=lastname,
                        )
                    )
                pass
        cursor.close()
        conn.close()
        error_message = "Invalid username or password"
        return render_template("login.html", error=error_message)
    return render_template("login.html", admin=admin, faculty=faculty, student=student)


@app.route("/home/student/<username>/<firstname>/<lastname>", endpoint="student_home")
def student_home(username, firstname, lastname):
    return render_template(
        "home-student.html", username=username, firstname=firstname, lastname=lastname
    )


@app.route("/home/faculty/<username>/<firstname>/<lastname>", endpoint="faculty_home")
def faculty_home(username, firstname, lastname):
    return render_template(
        "home-faculty.html", username=username, firstname=firstname, lastname=lastname
    )


@app.route("/home/admin/<username>/<firstname>/<lastname>", endpoint="admin_home")
def admin_home(username, firstname, lastname):
    return render_template(
        "home-admin.html", username=username, firstname=firstname, lastname=lastname
    )

@app.route("/profile")
def profile():
 return render_template("profile.html")

@app.route("/grades")
def grades():
 return render_template("grades.html")


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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            date,
            student_id,
            attendance_status
        )
    """
    )
    for row in sheet.iter_rows(min_row=2):
        date, student_id, attendance_status = row
        cursor.execute(
            "INSERT INTO attendance VALUES (?, ?, ?)",
            (date, student_id, attendance_status),
        )
    conn.commit()
    conn.close()
    message = "File uploaded successfully!"
    return render_template("upload.html", message=message)


@app.route("/attendance")
def attendance():
    date = request.args.get("date")
    attendance_data = get_attendance_data(date)
    return render_template("attendance.html", attendance_data=attendance_data)

def get_attendance_data(date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date, student_id, attendance_status FROM attendance WHERE date = ?", (date,))
    attendance_data = cursor.fetchall()
    connection.close()
    return attendance_data

@app.route("/courses")
def courses():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)


if __name__ == "__main__":
    app.run(debug=True)
