require('../tasks/static/tasks/js/dayViewPopUp.js'); 

beforeEach(() => 
{
    document.body.innerHTML = `
        <div id="calendar-body">
        <button id="day-view-close-btn"></button>
        `;

    document.dispatchEvent(new Event('DOMContentLoaded'));
});


describe('DOM Loaded Event attaches event listeners to calendar body and day view close button.', () => 
{
    test('adds event listener to calendar body when DOM content is loaded', () => 
    {
        const calendarBody = document.getElementById('calendar-body');
        expect(calendarBody).toHaveProperty('addEventListener');
    });

    test('adds event listeners today view close button when DOM content is loaded', () => 
    {
        const closeButton  = document.getElementById('day-view-close-btn');
        expect(closeButton).toHaveProperty('addEventListener');
    });
});

