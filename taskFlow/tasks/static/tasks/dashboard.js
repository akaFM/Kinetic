document.addEventListener('DOMContentLoaded', () => {
    const calendarDays = document.querySelectorAll('.calendar-day.has-tasks');
    
    calendarDays.forEach(day => {
        day.addEventListener('click', () => {
            const tasks = JSON.parse(day.dataset.tasks);
            const date = day.dataset.date;
            const modal = new bootstrap.Modal(document.getElementById('taskModal'));
            
            document.getElementById('modalDate').textContent = date;
            const taskDetails = document.getElementById('taskDetails');
            taskDetails.innerHTML = '';
            
            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.className = 'modal-task-item';
                taskElement.innerHTML = `
                    <h6>${task.description}</h6>
                    <div class="text-muted">
                        <span class="badge bg-primary">${task.type}</span>
                        <span class="ms-2">Due: ${new Date(task.due_date).toLocaleDateString()}</span>
                    </div>
                    <div class="mt-1">
                        Urgency: ${'★'.repeat(task.urgency)}${'☆'.repeat(5 - task.urgency)}
                    </div>
                `;
                taskDetails.appendChild(taskElement);
            });
            
            modal.show();
        });
    });
});