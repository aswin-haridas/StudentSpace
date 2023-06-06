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
                    fullname = f"{firstname} {lastname}"  # Merge first name and last name
                    return redirect(
                        url_for(
                            "student_home",
                            username=username,
                            fullname=fullname,
                        )
                    )
            elif user_type == "faculty":
                cursor.execute(
                    "SELECT firstname, lastname FROM facultylist WHERE id=?", (user_id,)
                )
                user_info = cursor.fetchone()
                if user_info is not None:
                    firstname, lastname = user_info
                    fullname = f"{firstname} {lastname}"  # Merge first name and last name
                    return redirect(
                        url_for(
                            "faculty_home",
                            username=username,
                            fullname=fullname,
                        )
                    )
            elif user_type == "admin":
                cursor.execute(
                    "SELECT firstname, lastname FROM facultylist WHERE id=?", (user_id,)
                )
                user_info = cursor.fetchone()
                if user_info is not None:
                    firstname, lastname = user_info
                    fullname = f"{firstname} {lastname}"  # Merge first name and last name
                    return redirect(
                        url_for(
                            "admin_home",
                            username=username,
                            fullname=fullname,
                        )
                    )
        cursor.close()
        conn.close()
        error_message = "Invalid username or password"
        return render_template("login.html", error=error_message)
    return render_template("login.html", admin=admin, faculty=faculty, student=student)


@app.route("/home/student/<username>/<fullname>", endpoint="student_home")
def student_home(username, fullname):
    return render_template(
        "home-student.html", username=username, fullname=fullname
    )


@app.route("/home/faculty/<username>/<fullname>", endpoint="faculty_home")
def faculty_home(username, fullname):
    return render_template(
        "home-faculty.html", username=username, fullname=fullname
    )


@app.route("/home/admin/<username>/<fullname>", endpoint="admin_home")
def admin_home(username, fullname):
    return render_template(
        "home-admin.html", username=username, fullname=fullname
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

 
@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    selected_day = request.args.get('day')
    if selected_day is None:
        selected_day = "1" 
    
    cursor.execute("SELECT DISTINCT date FROM attendance")
    dates = cursor.fetchall()
    days = [str(date[0]) for date in dates]

    cursor.execute("SELECT studentid, attendance_status FROM attendance WHERE date=?", (selected_day,))
    rows = cursor.fetchall()
    
    attendance_data = {}
    for row in rows:
        student_id = row[0]
        attendance_status = row[1]

        attendance_data[student_id] = attendance_status

    conn.close()
    return render_template("attendance.html", attendance_data=attendance_data, days=days, selected_day=selected_day)


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
