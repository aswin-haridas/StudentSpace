const testTypeDropdown = document.getElementById('test-type');
const table = document.getElementById('results-table');

testTypeDropdown.addEventListener('change', () => {
  const testType = testTypeDropdown.value;
  // Make an API call to get the updated data based on the selected test type
  // ...

  // Update the table with the new data
  table.innerHTML = ''; // Clear the table first
  const headerRow = table.insertRow();
  const courseNameHeader = headerRow.insertCell();
  courseNameHeader.innerHTML = 'Course Name';
  const gradeHeader = headerRow.insertCell();
  gradeHeader.innerHTML = 'Grade';
  const overallGradeHeader = headerRow.insertCell();
  overallGradeHeader.innerHTML = 'Overall Grade';
  const classAverageHeader = headerRow.insertCell();
  classAverageHeader.innerHTML = 'Class Average';
  const percentageHeader = headerRow.insertCell();
  percentageHeader.innerHTML = '%';

  // Loop through the data and add a row for each course
  for (const course of data) {
    const row = table.insertRow();
    const courseNameCell = row.insertCell();
    courseNameCell.innerHTML = course.name;
    const gradeCell = row.insertCell();
    gradeCell.innerHTML = course.grade;
    const overallGradeCell = row.insertCell();
    overallGradeCell.innerHTML = course.overallGrade;
    const classAverageCell = row.insertCell();
    classAverageCell.innerHTML = course.classAverage;
    const percentageCell = row.insertCell();
    percentageCell.innerHTML = course.percentage;
  }
});
