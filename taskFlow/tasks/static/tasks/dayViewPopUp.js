document.addEventListener('DOMContentLoaded', () => {

    const calendarBody = document.getElementById('calendar-body'     );
    const closeButton  = document.getElementById('day-view-close-btn');

    calendarBody.addEventListener('click', handleCalendarDayOnClick       );
    closeButton.addEventListener ('click', handleDayViewCloseButtonOnClick);
});

function handleDayViewCloseButtonOnClick()
{
    const calendarDayView  = document.getElementById('calendar-day-view');

    // Before day view pop up is closed, we must reset it for future use (when another day is clicked again).
    clearDayViewPop(); 
    hideElement(calendarDayView);
}

function showDayView(date) {
    const dayView = document.getElementById('calendar-day-view');
    const dayViewTitle = document.getElementById('title-day');
    const dayViewDate = document.getElementById('title-date');
    const taskContainer = document.getElementById('day-view-task-container');
    
    // Format the date for display
    const dateObj = new Date(date);
    const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
    const formattedDate = dateObj.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    
    // Update the title and date
    dayViewTitle.textContent = dayName;
    dayViewDate.textContent = formattedDate;
    
    // Clear previous content
    taskContainer.innerHTML = '';
    
    // Get tasks for this date from our Django-provided data
    const tasksForDay = tasksData[date] || [];
    
    if (tasksForDay.length === 0) {
        // Show "No tasks" message
        const noTasksMessage = document.createElement('div');
        noTasksMessage.className = 'no-tasks-message';
        noTasksMessage.textContent = 'No tasks on this day!';
        taskContainer.appendChild(noTasksMessage);
    } else {
        // Create elements for each task
        tasksForDay.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = 'day-view-task';
            
            taskElement.innerHTML = `
                <div class="task-header">
                    <span class="task-type ${task.type.toLowerCase()}">${task.type}</span>
                    <span class="task-urgency">Urgency: ${task.urgency}</span>
                </div>
                <div class="task-description">${task.description}</div>
            `;
            
            taskContainer.appendChild(taskElement);
        });
    }
    
    dayView.style.display = 'flex';
}

// Close button handler
document.getElementById('day-view-close-btn').onclick = function() {
    document.getElementById('calendar-day-view').style.display = 'none';
};

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