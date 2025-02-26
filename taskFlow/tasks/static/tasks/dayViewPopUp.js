document.addEventListener('DOMContentLoaded', () => {

    const calendarBody = document.getElementById('calendar-body'     );
    const closeButton  = document.getElementById('day-view-close-btn');

    calendarBody.addEventListener('click', handleCalendarDayOnClick       );
    closeButton.addEventListener ('click', handleDayViewCloseButtonOnClick);
});


function handleCalendarDayOnClick(event)
{
    const target = event.target;

    // Checks if the click event that occured on the calendar was on one of its days (a <td> element): 
    if (target.tagName === 'TD' && target.textContent.trim() !== '')
    {
        const dayNumber  = target.cellIndex;
        const dateNumber = target.textContent.trim();
        const dayString  = getDay(dayNumber);

        // Creates(updates) day view pop up window with appropriate day info:
        updateDayView(dateNumber, dayString);
    }
}


function handleDayViewCloseButtonOnClick()
{
    const calendarDayView  = document.getElementById('calendar-day-view');

    // Before day view pop up is closed, we must reset it for future use (when another day is clicked again).
    clearDayViewPop(); 
    hideElement(calendarDayView);
}


function updateDayView(dateNumber, dayString)
{
    const calendarDayView        = document.getElementById('calendar-day-view');
    const calendarTitleMonthYear = document.getElementById('calendar-month').innerText;
    const [month, year] = calendarTitleMonthYear.split(' ');
    
    updateDayViewTitle(dateNumber, dayString, month, year);
    getDayViewTasks(dateNumber, month, year); 
    showElement(calendarDayView);
}


function updateDayViewTitle(dateNumber, dayString, month, year)
{
    const dayTitle  = document.getElementById('title-day');
    const dateTitle = document.getElementById('title-date');

    // Set the day view pop title to match the day that was clicked on: 
    dayTitle.innerText  = dayString;
    dateTitle.innerText = `${dateNumber} ${month} ${year}`;
}


function getDayViewTasks(dateNumber, monthStr, yearStr)
{
    const day   = dateNumber;
    const year  = getYearNumber(yearStr);
    const month = getMonthNumber(monthStr);

    const dayViewTasks = document.getElementById('day-view-task-container');

    // Get tasks from backend for the specific day:
    fetch(`/tasks/${year}/${month}/${day}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.tasks.length > 0)
                for (let i = 0 ; i < data.tasks.length ; i++) // if day has tasks, then create elements for them.
                    createTaskElement(dayViewTasks, data.tasks[i].description);
            else
                createNoTasksElem(dayViewTasks); // if day has no tasks, then no task elements created.
        })
        .catch( error => console.error("Error fetching tasks.", error));
}


function createTaskElement(element, description)
{
    const taskContainer = document.createElement('div');
    taskContainer.classList.add('task-container');
    const taskText = document.createElement('span');
    taskText.classList.add('task-text');
    if (description.length < 50)
        taskText.textContent = description;  
    else
        taskText.textContent = description.slice(0, 49) + "..."; 
    taskContainer.appendChild(taskText);
    element.appendChild(taskContainer);
}


function createNoTasksElem(element)
{
    const noTask = document.createElement('div');
    noTask.textContent = 'No tasks.';  
    element.appendChild(noTask);
}


function getYearNumber(year)
{
    return parseInt(year);
}


function getMonthNumber(month)
{
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return months.indexOf(month) + 1;
}


function clearDayViewPop()
{
    const dayViewTasks     = document.getElementById('day-view-task-container');
    dayViewTasks.innerHTML = "";
}


function showElement(element)
{
    element.style.display = "block";
}


function hideElement(element)
{
    element.style.display = "none";
}


function getDay(dayOfWeek)
{
    const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday","Sunday"];
    return daysOfWeek[dayOfWeek];
}