import pandas as pd
from openpyxl import load_workbook
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    attendance_status = db.Column(db.Boolean, nullable=False)


workbook = load_workbook(filename="attendance.xlsx")
sheet = workbook["Attendance-January"]
df = pd.DataFrame(sheet.values, columns=["student_id", "date", "attendance_status"])

for index, row in df.iterrows():
    attendance = Attendance(
        student_id=row["student_id"],
        date=row["date"],
        attendance_status=bool(int(row["attendance_status"])),
    )
    db.session.add(attendance)
db.session.commit()
