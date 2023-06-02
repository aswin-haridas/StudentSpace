# import random, pandas as pd, datetime, timedelta, os

# attendance_status = [0, 1]
# start_date = datetime(2023, 5, 1)
# end_date = datetime(2023, 5, 31)
# dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# data = {
#     'student_id': ['CS10'] * len(dates),
#     'date': dates,
#     'attendance_status': random.choices(attendance_status, k=len(dates))
# }
# df = pd.DataFrame(data)

# if os.path.isfile('attendance_data.xlsx'):
#     existing_df = pd.read_excel('attendance_data.xlsx', engine='openpyxl')
#     df = pd.concat([existing_df, df], ignore_index=True)

# df.to_excel('attendance_data.xlsx', index=False)

# import pandas as pd
# import sqlite3

# excel_file = 'facultylist.xlsx'
# sheet_name = 'Sheet1'
# df = pd.read_excel(excel_file, sheet_name)

# db_file = 'database.db'
# conn = sqlite3.connect(db_file)
# df.to_sql('facultylist', conn, if_exists='replace', index=False)

# conn.close()


import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "courses" table
cursor.execute('''CREATE TABLE courses (
                    course_id INTEGER PRIMARY KEY,
                    course_name TEXT,
                    instructor TEXT,
                    credits INTEGER
                )''')

# Sample data for computer science courses
course_data = [
    (1, 'Introduction to Programming', 'John Smith', 4),
    (2, 'Data Structures', 'Jane Doe', 3),
    (3, 'Database Management', 'Robert Johnson', 3),
    (4, 'Algorithms', 'Sarah Thompson', 4),
    (5, 'Operating Systems', 'Michael Brown', 3)
]

# Insert the sample data into the "courses" table
cursor.executemany('INSERT INTO courses VALUES (?, ?, ?, ?)', course_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
