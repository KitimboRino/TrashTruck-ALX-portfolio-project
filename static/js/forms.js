document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-messages .flash-message');
    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.classList.add('fade');
        }, 3000); // Adjust the delay (in milliseconds) as needed
    });
});

// Login validation
document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');
    var emailInput = document.getElementById('email');
    var passwordInput = document.getElementById('password');
    var emailError = document.getElementById('emailError');
    var passwordError = document.getElementById('passwordError');

    loginForm.addEventListener('submit', function (event) {
        var email = emailInput.value;
        var password = passwordInput.value;
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            emailError.classList.remove('d-none');
            event.preventDefault();
        } else {
            emailError.classList.add('d-none');
        }

        if (password.length < 6) {
            passwordError.classList.remove('d-none');
            event.preventDefault();
        } else {
            passwordError.classList.add('d-none');
        }
    });

});

