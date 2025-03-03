const editTasks = require('../tasks/static/tasks/js/edit_tasks.js');

describe('ONE TIME TASKS:', () => 
{
    let container;
    let fields;
    let displays;
    let editBtn;
    let saveBtn;
    let cancelBtn;

    function setupDOM() 
    {
        document.body.innerHTML = `
            <div id="task-1">
                <h5 class="task-name">Task name</h5>
                <p class="task-description">Task description</p>
                <span class="due-date">March 02, 2025</span>
                <span class="task-type">Work</span>
                <span class="task-urgency">1</span>
                <input class="edit-field" style="display: none" />
                <button class="edit-btn">Edit</button>
                <button class="save-btn" style="display: none">Save</button>
                <button class="cancel-btn" style="display: none">Cancel</button>
            </div>
        `;

        container = document.getElementById('task-1');
        fields    = container.getElementsByClassName('edit-field');
        displays  = container.querySelectorAll('.task-name, .due-date, .task-type, .task-urgency, .task-description');
        editBtn   = container.querySelector('.edit-btn');
        saveBtn   = container.querySelector('.save-btn');
        cancelBtn = container.querySelector('.cancel-btn');
    }

    beforeEach(setupDOM);

    describe('toggleEdit() tests', () => 
    {
        test('shows edit fields when edit button clicked', () => {
            editTasks.toggleEdit(1, false);
            Array.from(fields).forEach(field => { expect(field.style.display).toBe('inline-block'); });
        });

        test('hides displays when edit button clicked', () => {
            editTasks.toggleEdit(1, false);
            Array.from(displays).forEach(display => { expect(display.style.display).toBe('none'); });
        });

        test('hides edit button when edit button clicked', () => {
            editTasks.toggleEdit(1, false);
            expect(editBtn.style.display).toBe('none');
        });

        test('shows save button when edit button clicked', () => {
            editTasks.toggleEdit(1, false);
            expect(saveBtn.style.display).toBe('inline-block');
        });

        test('shows cancel button when edit button clicked', () => {
            editTasks.toggleEdit(1, false);
            expect(cancelBtn.style.display).toBe('inline-block');
        });
    });

    describe('cancelEdit() tests', () => 
    {
        test('hides edit fields when cancel button clicked', () => {
            editTasks.cancelEdit(1, false);
            Array.from(fields).forEach(field => { expect(field.style.display).toBe('none'); });
        });

        test('shows displays when cancel button clicked', () => {
            editTasks.cancelEdit(1, false);
            Array.from(displays).forEach(display => { expect(display.style.display).toBe('inline'); });
        });

        test('shows edit button when cancel button clicked', () => {
            editTasks.cancelEdit(1, false);
            expect(editBtn.style.display).toBe('inline-block');
        });

        test('hides save button when cancel button clicked', () => {
            editTasks.cancelEdit(1, false);
            expect(saveBtn.style.display).toBe('none');
        });

        test('hides cancel button when cancel button clicked', () => {
            editTasks.cancelEdit(1, false);
            expect(cancelBtn.style.display).toBe('none');
        });
    });
});




describe('RECURRING TASKS:', () => 
{
    let container;
    let fields;
    let displays;
    let editBtn;
    let saveBtn;
    let cancelBtn;

    function setupDOM() 
    {
        document.body.innerHTML = `
            <div id="pattern-1">
                <h5 class="task-name">Task name</h5>
                <p class="task-description">Task description</p>
                <span class="due-date">March 02, 2025</span>
                <span class="task-type">Work</span>
                <span class="task-urgency">1</span>
                <input class="edit-field" style="display: none" />
                <button class="edit-btn">Edit</button>
                <button class="save-btn" style="display: none">Save</button>
                <button class="cancel-btn" style="display: none">Cancel</button>
            </div>
        `;

        container = document.getElementById('pattern-1');
        fields    = container.getElementsByClassName('edit-field');
        displays  = container.querySelectorAll('.task-name, .due-date, .task-type, .task-urgency, .task-description');
        editBtn   = container.querySelector('.edit-btn');
        saveBtn   = container.querySelector('.save-btn');
        cancelBtn = container.querySelector('.cancel-btn');
    }

    beforeEach(setupDOM);

    describe('toggleEdit() tests', () => 
    {
        test('shows edit fields when edit button clicked', () => {
            editTasks.toggleEdit(1, true);
            Array.from(fields).forEach(field => { expect(field.style.display).toBe('inline-block'); });
        });

        test('hides displays when edit button clicked', () => {
            editTasks.toggleEdit(1, true);
            Array.from(displays).forEach(display => { expect(display.style.display).toBe('none'); });
        });

        test('hides edit button when edit button clicked', () => {
            editTasks.toggleEdit(1, true);
            expect(editBtn.style.display).toBe('none');
        });

        test('shows save button when edit button clicked', () => {
            editTasks.toggleEdit(1, true);
            expect(saveBtn.style.display).toBe('inline-block');
        });

        test('shows cancel button when edit button clicked', () => {
            editTasks.toggleEdit(1, true);
            expect(cancelBtn.style.display).toBe('inline-block');
        });
    });

    describe('cancelEdit() tests', () => 
    {
        test('hides edit fields when cancel button clicked', () => {
            editTasks.cancelEdit(1, true);
            Array.from(fields).forEach(field => { expect(field.style.display).toBe('none'); });
        });

        test('shows displays when cancel button clicked', () => {
            editTasks.cancelEdit(1, true);
            Array.from(displays).forEach(display => { expect(display.style.display).toBe('inline'); });
        });

        test('shows edit button when cancel button clicked', () => {
            editTasks.cancelEdit(1, true);
            expect(editBtn.style.display).toBe('inline-block');
        });

        test('hides save button when cancel button clicked', () => {
            editTasks.cancelEdit(1, true);
            expect(saveBtn.style.display).toBe('none');
        });

        test('hides cancel button when cancel button clicked', () => {
            editTasks.cancelEdit(1, true);
            expect(cancelBtn.style.display).toBe('none');
        });
    });
});