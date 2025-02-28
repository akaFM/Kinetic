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
                    createTaskElement(dayViewTasks, data.tasks[i]);
            else
                createNoTasksElem(dayViewTasks); // if day has no tasks, then no task elements created.
        })
        .catch( error => console.error("Error fetching tasks.", error));
}


function createTaskElement(element, task)
{
    const taskContainer = document.createElement('div');
    taskContainer.classList.add('task-container');
    if (task.completed) {
        taskContainer.classList.add('completed');
    }

    // Create task header
    const taskHeader = document.createElement('div');
    taskHeader.classList.add('task-header');

    // Create header content container
    const taskHeaderContent = document.createElement('div');
    taskHeaderContent.classList.add('task-header-content');

    // Add task name
    const taskName = document.createElement('div');
    taskName.classList.add('task-name');
    taskName.textContent = task.name;
    taskHeaderContent.appendChild(taskName);

    // Add task urgency
    const taskUrgency = document.createElement('div');
    taskUrgency.classList.add('task-urgency');
    taskUrgency.textContent = `Priority ${task.urgency}`;
    taskHeaderContent.appendChild(taskUrgency);

    taskHeader.appendChild(taskHeaderContent);

    // Add complete button
    const completeBtn = document.createElement('button');
    completeBtn.classList.add('complete-task-btn');
    if (task.completed) {
        completeBtn.classList.add('completed');
        completeBtn.innerHTML = '✓';
        completeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            uncompleteTask(task.id, taskContainer);
        });
    } else {
        completeBtn.innerHTML = '✓';
        completeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            completeTask(task.id, taskContainer);
        });
    }
    taskHeader.appendChild(completeBtn);

    taskContainer.appendChild(taskHeader);

    // Add task description
    const taskDescription = document.createElement('div');
    taskDescription.classList.add('task-description');
    taskDescription.textContent = task.description;
    taskContainer.appendChild(taskDescription);

    // Add task type
    const taskType = document.createElement('div');
    taskType.classList.add('task-type');
    taskType.textContent = `Type: ${task.type}`;
    taskContainer.appendChild(taskType);

    element.appendChild(taskContainer);
}


function createNoTasksElem(element)
{
    const noTask = document.createElement('div');
    noTask.classList.add('no-tasks');
    noTask.textContent = 'No tasks scheduled for this day.';
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

async function completeTask(taskId, taskContainer) {
    try {
        const response = await fetch('/tasks/complete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                task_id: taskId
            })
        });

        if (response.ok) {
            taskContainer.classList.add('completed');
            const completeBtn = taskContainer.querySelector('.complete-task-btn');
            completeBtn.classList.add('completed');
            completeBtn.disabled = true;
        }
    } catch (error) {
        console.error('Error completing task:', error);
    }
}

async function uncompleteTask(taskId, taskContainer) {
    try {
        const response = await fetch('/tasks/uncomplete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                task_id: taskId
            })
        });

        if (response.ok) {
            taskContainer.classList.remove('completed');
            const completeBtn = taskContainer.querySelector('.complete-task-btn');
            completeBtn.classList.remove('completed');
            
            // Remove old event listener and add new one
            const newBtn = completeBtn.cloneNode(true);
            newBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                completeTask(taskId, taskContainer);
            });
            completeBtn.parentNode.replaceChild(newBtn, completeBtn);
        }
    } catch (error) {
        console.error('Error uncompleting task:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}