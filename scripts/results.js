const xlsx = require('xlsx');
const sqlite3 = require('sqlite3').verbose();

// Open the xlsx file and get the first sheet
const workbook = xlsx.readFile('data.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];

// Create an array of objects representing the rows in the sheet
const rows = xlsx.utils.sheet_to_json(sheet, { header: 1 });

// Connect to the database and create a table
const db = new sqlite3.Database('database.db');
db.run(`
  CREATE TABLE IF NOT EXISTS results (
    course_name TEXT,
    grade INTEGER,
    overall_grade INTEGER,
    class_average INTEGER,
    percentage INTEGER
  )
`);

// Insert each row into the database table
for (let row of rows) {
  db.run(`
    INSERT INTO results (course_name, grade, overall_grade, class_average, percentage)
    VALUES (?, ?, ?, ?, ?)
  `, row);
}

// Close the database connection
db.close();
