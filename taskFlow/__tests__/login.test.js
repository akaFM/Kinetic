require('../tasks/static/tasks/js/login.js'); 

describe('Login.js Tests', () => 
{
    let userInputField;
    let passwordInputField;

    // SETUP:
    beforeEach( () => 
    {
        document.body.innerHTML = `
          <input type="text" id="login-user" placeholder="Enter your username">
          <input type="password" id="login-password" placeholder="Enter your password">`;

        document.dispatchEvent(new window.Event('DOMContentLoaded'));

        userInputField     = document.getElementById('login-user');
        passwordInputField = document.getElementById('login-password');
    });



    test('handleInputFieldFocus() clears login username field placeholder', () => 
    {
        userInputField.focus();
        expect(userInputField.placeholder).toBe('');
    });


    test('handleInputFieldFocus() clears login passord field placeholder', () => 
    {
        passwordInputField.focus();
        expect(passwordInputField.placeholder).toBe('');
    });


    test('handleInputFieldBlur() sets login username correct placeholder', () => 
    {
        userInputField.blur();
        expect(userInputField.placeholder).toBe('Enter your username');
    });


    test('handleInputFieldBlur() sets login password correct placeholder', () => 
    {
        passwordInputField.blur();
        expect(passwordInputField.placeholder).toBe('Enter your password');
    });


    test('focus event listener is attached to login username field on DOMContentLoaded', () => 
    {
        userInputField.dispatchEvent(new window.Event('focus'));
        expect(userInputField.placeholder).toBe('');
    });


    test('blur event listener is attached to login username field on DOMContentLoaded', () => 
    {
        userInputField.dispatchEvent(new window.Event('blur'));
        expect(userInputField.placeholder).toBe('Enter your username');
    });


    test('focus event listener is attached to login password field on DOMContentLoaded', () => 
    {
        passwordInputField.dispatchEvent(new window.Event('focus'));
        expect(passwordInputField.placeholder).toBe('');
    });


    test('blur event listener is attached to login password field on DOMContentLoaded', () => 
    {
        passwordInputField.dispatchEvent(new window.Event('blur'));
        expect(passwordInputField.placeholder).toBe('Enter your password');
    });
});