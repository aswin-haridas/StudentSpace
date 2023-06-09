from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from openpyxl import load_workbook
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key_here"


@app.context_processor
def common_icons():
    admin = "/static/assets/admin.png"
    student = "/static/assets/student.png"
    faculty = "/static/assets/faculty.png"
    search = "/static/assets/search.png"
    notification = "/static/assets/notification.png"
    settings = "/static/assets/settings.png"
    return dict(
        search=search,
        notification=notification,
        settings=settings,
        admin=admin,
        faculty=faculty,
        student=student,
    )


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_type_form = request.form.get("user-type")
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, role, username FROM users WHERE username=? AND password=?",
            (username, password),
        )
        result = cursor.fetchone()

        if result is not None:
            user_id, user_type, name = result
            session["user_id"] = user_id
            session["user_type"] = user_type
            session["username"] = username
            session["name"] = name

            if user_type_form == user_type:
                return redirect(url_for("home"))
        error_message = "Invalid username or password"
        return render_template("error.html", error=error_message)

    return render_template("login.html")


@app.route("/home", endpoint="home")
def home():
    user_id = session.get("user_id")
    user_type =session.get("user_type")
    username = session.get("username")
    name = session.get("name")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if user_type == "student":
        cursor.execute("SELECT name FROM studentlist WHERE id=?", (user_id,))
    elif user_type == "faculty":
        cursor.execute("SELECT name FROM facultylist WHERE id=?", (user_id,))

    result = cursor.fetchone()
    fullname = None
    if result is not None:
        fullname = result[0]

    conn.close()

    return render_template(
        "home.html",
        username=username,
        name=name,
        user_type=user_type,
        fullname=fullname,
    )


@app.route("/grades")
def get_student_grades():
    user_id = session.get("user_id")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM grades WHERE id = ?", (user_id,))
    data = c.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/perfomance")
def perfomance():
    user_id = session.get("user_id")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade WHERE id = ?", (user_id,))
    marks = cursor.fetchone()  # Extracting the marks from the query result
    return render_template("perfomance.html", marks=marks)


@app.route("/profile")
def profile():
    user_id = session.get("user_id")  # Retrieve the user_id from the session
    if user_id is None:
        return "User ID not found"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM studentlist WHERE id=?", (user_id,))
    student_info = cursor.fetchone()
    conn.close()

    if student_info is not None:
        id = student_info[0]
        name = student_info[1]
        dob = student_info[2]
        email = student_info[3]
        course = student_info[4]
        contact = student_info[5]
        address = student_info[6]

        return render_template(
            "profile.html",
            id=id,
            name=name,
            dob=dob,
            email=email,
            course=course,
            contact=contact,
            address=address,
        )

    return "Student not found"


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


@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    selected_day = request.args.get("day")
    if selected_day is None:
        selected_day = "1"

    cursor.execute("SELECT DISTINCT date FROM attendance")
    dates = cursor.fetchall()
    days = [str(date[0]) for date in dates]

    cursor.execute(
        "SELECT studentid, attendance_status FROM attendance WHERE date=?",
        (selected_day,),
    )
    rows = cursor.fetchall()

    attendance_data = {}
    for row in rows:
        student_id = row[0]
        attendance_status = row[1]

        attendance_data[student_id] = attendance_status

    conn.close()
    return render_template(
        "attendance.html",
        attendance_data=attendance_data,
        days=days,
        selected_day=selected_day,
    )


@app.route("/courses")
def courses():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses_data = cursor.fetchall()
    conn.close()
    return render_template("courses.html", courses=courses_data)

@app.route('/logout' )
def logout():
    session.clear() 
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
 