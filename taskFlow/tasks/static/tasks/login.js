document.addEventListener('DOMContentLoaded', () => {
    const authMessage = document.getElementById('authMessage');
    if (authMessage) {
        if (authMessage.textContent.toLowerCase().includes('invalid') || 
            authMessage.textContent.toLowerCase().includes('error')) {
            authMessage.classList.add('error');
        }
    }
    
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', () => {
            input.placeholder = '';
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.placeholder = input.type === 'text' ? 'Enter your username' : 'Enter your password';
            }
        });
    });
});