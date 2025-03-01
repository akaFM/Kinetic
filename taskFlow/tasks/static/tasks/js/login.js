document.addEventListener('DOMContentLoaded', () => {
    const user_input_field = document.getElementById('login-user');
    user_input_field.addEventListener('focus',handleInputFieldFocus);
    user_input_field.addEventListener('blur',handleInputFieldBlur);

    const password_input_field = document.getElementById('login-password');
    password_input_field.addEventListener('focus',handleInputFieldFocus);
    password_input_field.addEventListener('blur',handleInputFieldBlur);
});

function handleInputFieldBlur(event)
{
    event.target.placeholder = event.target.type === 'text' ? 'Enter your username' : 'Enter your password';
}

function handleInputFieldFocus(event)
{
    event.target.placeholder = '';
}