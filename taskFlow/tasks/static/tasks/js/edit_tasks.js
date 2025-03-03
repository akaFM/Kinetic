function toggleEdit(id, isRecurring) {
    const container = document.getElementById(isRecurring ? `pattern-${id}` : `task-${id}`);
    const fields = container.getElementsByClassName('edit-field');
    const displays = container.querySelectorAll('.task-name, .due-date, .task-type, .task-urgency, .task-description');
    const editBtn = container.querySelector('.edit-btn');
    const saveBtn = container.querySelector('.save-btn');
    const cancelBtn = container.querySelector('.cancel-btn');

    Array.from(fields).forEach(field => field.style.display = 'inline-block');
    Array.from(displays).forEach(display => display.style.display = 'none');
    
    editBtn.style.display = 'none';
    saveBtn.style.display = 'inline-block';
    cancelBtn.style.display = 'inline-block';
}

function cancelEdit(id, isRecurring) {
    const container = document.getElementById(isRecurring ? `pattern-${id}` : `task-${id}`);
    const fields = container.getElementsByClassName('edit-field');
    const displays = container.querySelectorAll('.task-name, .due-date, .task-type, .task-urgency, .task-description');
    const editBtn = container.querySelector('.edit-btn');
    const saveBtn = container.querySelector('.save-btn');
    const cancelBtn = container.querySelector('.cancel-btn');

    // Hide edit fields, show display text
    Array.from(fields).forEach(field => field.style.display = 'none');
    Array.from(displays).forEach(display => display.style.display = 'inline');
    
    // Show edit button, hide save/cancel buttons
    editBtn.style.display = 'inline-block';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
}

module.exports = { toggleEdit, cancelEdit }; 