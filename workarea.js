const calendar = document.querySelector(".calendar");
const monthYear = calendar.querySelector(".month-year");
const prevMonthBtn = calendar.querySelector(".prev-month-btn");
const nextMonthBtn = calendar.querySelector(".next-month-btn");
const calendarGrid = calendar.querySelector(".calendar-grid");
const weekdays = calendarGrid.querySelector(".weekdays");

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

let currentDate = new Date();

function renderCalendar() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const lastDayOfPrevMonth = new Date(year, month, 0).getDate();

  monthYear.textContent = `${months[month]} ${year}`;

  // Clear previous calendar days
  calendarGrid.innerHTML = "";

  // Render weekdays
  for (let i = 0; i < daysOfWeek.length; i++) {
    const day = document.createElement("div");
    day.textContent = daysOfWeek[i];
    weekdays.appendChild(day);
  }

  // Render previous month days
  for (let i = firstDayOfMonth - 1; i >= 0; i--) {
    const day = document.createElement("div");
    day.textContent = lastDayOfPrevMonth - i;
    day.classList.add("prev-month-day");
    calendarGrid.appendChild(day);
  }

  // Render current month days
  for (let i = 1; i <= daysInMonth; i++) {
    const day = document.createElement("div");
    day.textContent = i;
    day.classList.add("calendar-day");
    if (
      i === currentDate.getDate() &&
      month === currentDate.getMonth() &&
      year === currentDate.getFullYear()
    ) {
      day.classList.add("today");
    }
    calendarGrid.appendChild(day);
  }

  // Render next month days
  const remainingCells = (7 - ((firstDayOfMonth + daysInMonth) % 7)) % 7;
  for (let i = 1; i <= remainingCells; i++) {
    const day = document.createElement("div");
    day.textContent = i;
    day.classList.add("next-month-day");
    calendarGrid.appendChild(day);
  }
}

renderCalendar();

prevMonthBtn.addEventListener("click", () => {
  currentDate = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() - 1,
    currentDate.getDate()
  );
  renderCalendar();
});

nextMonthBtn.addEventListener("click", () => {
  currentDate = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    currentDate.getDate()
  );
  renderCalendar();
});
