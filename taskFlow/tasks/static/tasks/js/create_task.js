function toggleRecurringFields() {
    const isRecurring = document.getElementById('id_is_recurring').checked;
    const recurringFields = document.getElementById('recurring-fields');
    const dueDateField = document.getElementById('due-date-field');
    const dueDateInput = document.getElementById('id_due_date');
    
    recurringFields.style.display = isRecurring ? 'block' : 'none';
    dueDateField.style.display = isRecurring ? 'none' : 'block';
    
    if (isRecurring) {
        dueDateInput.removeAttribute('required');
    } else {
        dueDateInput.setAttribute('required', 'required');
    }
}

// JavaScript for floating animation on task form fields
window.addEventListener('DOMContentLoaded', () => {
    const formFields = document.querySelectorAll('.form-field');
    formFields.forEach((field, index) => {
        setTimeout(() => {
            field.classList.add('animate');
        }, index * 200);
    });
});

// this is to ensure that the frontend does not allow urgency over 10 or under 1
document.addEventListener('DOMContentLoaded', function() {
    const urgencyInput = document.getElementById('id_urgency');
    
    urgencyInput.addEventListener('input', function() {
        let value = parseInt(this.value);
        if (value > 10) this.value = 10;
        if (value < 1 || isNaN(value)) this.value = 1;
    });
});

document.getElementById('id_is_recurring').addEventListener('change', toggleRecurringFields);

// this part is for the character counters in name and desc fields.
document.addEventListener('DOMContentLoaded', function() {
    function updateCharacterCount(input, counterId) {
        const counter = document.getElementById(counterId);
        const maxLength = input.getAttribute('maxlength');
        counter.textContent = `${input.value.length}/${maxLength}`;
    }

    const nameInput = document.getElementById('id_name');
    const descInput = document.getElementById('id_description');

    nameInput.addEventListener('input', () => updateCharacterCount(nameInput, 'name-counter'));
    descInput.addEventListener('input', () => updateCharacterCount(descInput, 'description-counter'));

    // Initialize counters
    updateCharacterCount(nameInput, 'name-counter');
    updateCharacterCount(descInput, 'description-counter');
});