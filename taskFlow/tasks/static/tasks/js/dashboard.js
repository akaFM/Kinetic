    function generateCalendar(targetDate = new Date()) {
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const firstDay = new Date(targetDate.getFullYear(), targetDate.getMonth(), 1).getDay();
        const daysInMonth = new Date(targetDate.getFullYear(), targetDate.getMonth() + 1, 0).getDate();

        document.getElementById("calendar-month").innerText = `${monthNames[targetDate.getMonth()]} ${targetDate.getFullYear()}`;
        document.getElementById("year-select").value = targetDate.getFullYear();

        let calendarBody = "";
        let date = 1;

        for (let i = 0; i < 6; i++) {
            let row = "<tr>";
            for (let j = 1; j <= 7; j++) {
                if ((i === 0 && j < firstDay) || date > daysInMonth) {
                    row += "<td></td>";
                } else {
                    const isToday = date === new Date().getDate() && 
                                targetDate.getMonth() === new Date().getMonth() && 
                                targetDate.getFullYear() === new Date().getFullYear();
                    row += `<td class="${isToday ? 'today' : ''}">${date}</td>`;
                    date++;
                }
            }
            row += "</tr>";
            calendarBody += row;
        }

        document.getElementById("calendar-body").innerHTML = calendarBody;

    }

    let currentDate = new Date();

    document.getElementById("prev-month").addEventListener("click", () => {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
        generateCalendar(currentDate);
    });

    document.getElementById("next-month").addEventListener("click", () => {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
        generateCalendar(currentDate);
    });

    window.onload = () => {
        populateYearDropdown();
        generateCalendar(currentDate);
    };

    function populateYearDropdown() {
        const yearSelect = document.getElementById('year-select');
        const currentYear = new Date().getFullYear();
        
        // add years (5 years before and after current year)
        for (let year = currentYear - 5; year <= currentYear + 5; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            if (year === currentYear) {
                option.selected = true;
            }
            yearSelect.appendChild(option);
        }

        yearSelect.addEventListener('change', () => {
            currentDate.setFullYear(parseInt(yearSelect.value));
            generateCalendar(currentDate);
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const categoryForm = document.getElementById('categoryForm');
        const categoryButtons = categoryForm.querySelectorAll('.category-btn');

        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons and set active on clicked button
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                // If the day view popup is open, clear its container and refresh its tasks:
                const calendarDayView = document.getElementById('calendar-day-view');
                if (calendarDayView && calendarDayView.style.display === "block") {
                    // Clear the popup container before fetching new tasks
                    const dayViewTasks = document.getElementById('day-view-task-container');
                    dayViewTasks.innerHTML = '';
                    
                    // Get the currently displayed date from the title (format: "day month year")
                    const dateTitleElem = document.getElementById('title-date');
                    if (dateTitleElem && dateTitleElem.innerText.trim() !== "") {
                        const [day, month, year] = dateTitleElem.innerText.split(' ');
                        getDayViewTasks(day, month, year);
                    }
                }
            });
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        const currentTimeElement = document.getElementById('current-time');
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        // Format hours and minutes to always show two digits.
        const formattedTime = ('0' + hours).slice(-2) + ':' + ('0' + minutes).slice(-2);
        currentTimeElement.innerText = `${formattedTime}`;
    });

    function updateTime() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = ('0' + now.getMinutes()).slice(-2);
        const seconds = ('0' + now.getSeconds()).slice(-2);
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // convert 0 to 12
        hours = ('0' + hours).slice(-2);
        const formattedTime = `${hours}:${minutes}:${seconds} ${ampm}`;
        document.getElementById('current-time').textContent = `${formattedTime} ⌛`;
    }
    updateTime(); // Initialize immediately
    setInterval(updateTime, 1000);