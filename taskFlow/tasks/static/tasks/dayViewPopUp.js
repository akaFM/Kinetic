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
    const calendarDayView = document.getElementById('calendar-day-view');
    
    updateDayViewTitle(dateNumber, dayString);
    getDayViewTasks(); // just creates 12 dummy tasks elements right now for demoing.
    showElement(calendarDayView);
}

function updateDayViewTitle(dateNumber, dayString)
{
    const dayTitle      = document.getElementById('title-day');
    const dateTitle     = document.getElementById('title-date');
    const calendarMonth = document.getElementById('calendar-month');
    const month         = calendarMonth.innerText;

    // Set the day view pop title to match the day that was clicked on: 
    dayTitle.innerText  = dayString;
    dateTitle.innerText = `${dateNumber} ${month}`;
}

function getDayViewTasks()
{
    const dayViewTasks = document.getElementById('day-view-task-container');

    // just creates 12 dummy tasks elements right now for demoing.
    for (let i = 0; i < 12; i++) 
    {
        const taskContainer = document.createElement('div');
        taskContainer.classList.add('task-container');
        const taskText = document.createElement('span');
        taskText.classList.add('task-text');
        taskText.textContent = `Task Description ${i + 1}`;  
        taskContainer.appendChild(taskText);
        dayViewTasks.appendChild(taskContainer);
    }
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