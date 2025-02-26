document.addEventListener('DOMContentLoaded', () => {

    // Handle focus and blur for input fields:
    const user_input_field = document.getElementById('login-user');
    user_input_field.addEventListener('focus',handleInputFieldFocus);
    user_input_field.addEventListener('blur',handleInputFieldBlur);

    const password_input_field = document.getElementById('login-password');
    password_input_field.addEventListener('focus',handleInputFieldFocus);
    password_input_field.addEventListener('blur',handleInputFieldBlur);

    // Check password has correct format before submitting it:
    const login_form = document.getElementById('login-form');
    login_form.addEventListener('submit', handlePasswordFormatValidation);
});


function handleInputFieldBlur(event)
{
    event.target.placeholder = event.target.type === 'text' ? 'Enter your username' : 'Enter your password';
}
function handleInputFieldFocus(event)
{
    event.target.placeholder = '';
}

function handlePasswordFormatValidation(event)
{
    const login_password = document.getElementById('login-password');
    const password       = login_password.value;

    // REGEX:
    // 6-20 chars long
    // At least one uppercase
    // At least one lowercase
    // At least one number
    // At least one special char (no spaces) 
    const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{6,20}$/;

    if (!password_regex.test(password))
    {
        event.preventDefault(); // prevent from submitting.
        showElement(document.getElementById('invalid-password-msg')); // display error msg;
    }
    else
    {
        hideElement(document.getElementById('invalid-password-msg')); // hide error msg;
    }
}

function showElement(element)
{
    element.style.display = "block";
}

function hideElement(element)
{
    element.style.display = "none";
}