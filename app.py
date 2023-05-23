# login.html edk adhyam

# uploadil ninn aanu vannenki vaayicho

# aadhyam namk korch saathanangal import chyyam
# import chyaneth namma pip install vech install chytha items aaanu

from flask import Flask, render_template, request, redirect, url_for
import openpyxl
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
# ini flask enna application initialize chyaam

app = Flask(__name__)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)
# app route / set aakial namma ee code run chyyumba kanikkanda homepage aanu
# ee homepageum nammada homepageum ayit yaathoru benthom illa

@app.route('/', methods=['GET', 'POST'])
def login():
    admin='/static/assets/admin.png'
    student='/static/assets/student.png'
    faculty='/static/assets/faculty.png'

    if request.method == 'POST':
        # Perform login verification here
        user_type = request.form.get('user-type')
        username = request.form.get('username')
        password = request.form.get('password')
        # Verify the credentials and redirect to appropriate page
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM studentlist WHERE username=? AND password=?',
                       (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is not None:
            name = result[0]
            if user_type == 'student':
                return redirect(url_for('student_home', name=name))
            elif user_type == 'faculty':
                return redirect(url_for('faculty_home', name=name))
            elif user_type == 'admin':
                return redirect(url_for('admin_home', name=name))

        # Credentials are incorrect, show an error message
        error_message = "Invalid username or password"
        return render_template('login.html', error=error_message)

    return render_template('login.html',admin=admin,faculty=faculty,student=student)


@app.route('/student-home/<name>', endpoint='student_home')
def student_home(name):
    return render_template('student-home.html', name=name)

@app.route('/faculty-home/<name>', endpoint='faculty_home')
def faculty_home(name):
    return render_template('faculty-home.html', name=name)

@app.route('/admin-home/<name>', endpoint='admin_home')
def admin_home(name):
    return render_template('admin-home.html', name=name)


@app.route("/upload")
def upload():
    return render_template("upload.html")


# ivide render template upload anu kodthekkane, sherikinum login aanu varande.(for the moment ingana aan)
# ini namma nerathe kanille upload chyan parayanath matte xl file..
# avidethe upload button press chyyyumbo ent sambavikanam ennanu thaze kodthekkane


@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    # namma upload chytha file load chyth file enn paranja variablilek idum

    wb = openpyxl.load_workbook(file)
    # ennit aa file openpyxl enna library vech open chyyum. enthinaa?
    # enthinaaa?
    # enthinaa? ath extract chyyande ennalalle databaseil idan pattullu

    sheet = wb.active
    # ennit athile sheet edkum. aake oru sheetey kaanullu

    conn = sqlite3.connect("database.db")
    # ennit namma database ayit connection indakum . set aakande

    cursor = conn.cursor()
    # a cursor is a control structure that allows us to interact with the SQLite database.hemme inklish
    # ee cursor vech namk database il read um write oke chyyam

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            date TEXT,
            student_id TEXT,
            attendance_status INTEGER
        )
    """
    )
    # ith namma attendance enna table indakkan aanu .already illenki indakkum illel athil thanne add chyum

    for row in sheet.iter_rows(min_row=2):
        date = row[0].value
        student_id = row[1].value
        attendance_status = row[2].value
        cursor.execute(
            "INSERT INTO attendance VALUES (?, ?, ?)",
            (date, student_id, attendance_status),
        )
        # ellam mansilayille. insert chythath aan
    conn.commit()
    # commit chythu
    conn.close()
    # connection verpirinju
    message = "File uploaded successfully!"
    # chumma oru message irikkate . ith avar kanumbalekkum exel sheetinn data mothom table il store ayitindavum
    return render_template(
        "upload.html", message=message
    )  # ini namma upload.html onnude render chyyth kanikum.

    # ee coma kainj enthelum ital ath html ilek pass chyyan aanu in this case "upload sucesful" aan message
    # ee message aan njan paranje %% oke kanum enn %% ittale html il ee pass chytha sambavam varullu


@app.route("/attendance")
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    attendance_data = cursor.fetchall()
    conn.close()
    return render_template("attendance.html", attendance_data=attendance_data)


# ee function enthinanen vecha database il poi attendance ile ella recordum select chythit attendance.html ilek pass chyyum
# ath namma avida display chyyum

if __name__ == "__main__":
    app.run(debug=True)
# app run kanumbo matte server varum 127:000 enna address olla sambavam
