document.getElementById('btn-signup').addEventListener('click', function() {
  document.querySelector('.form-signin').style.display = 'none';
  document.querySelector('.form-signup').style.display = 'block';
});

document.getElementById('cancel_signup').addEventListener('click', function() {
  document.querySelector('.form-signup').style.display = 'none';
  document.querySelector('.form-signin').style.display = 'block';
});

document.getElementById('cancel_signup').addEventListener('click', function() {
  document.querySelector('.form-signup').style.display = 'none';
  document.querySelector('.form-signin').style.display = 'block';
});

document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('login-form');
  loginForm.addEventListener('submit', function(event) {
    event.preventDefault();  // Предотвратить перезагрузку страницы

    const loginData = {
      email: document.getElementById('login-email').value,
      password: document.getElementById('login-password').value
    };
    const csrfToken = getCSRFToken();
    fetch('user_login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(loginData),
      credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        window.location.href = data.redirect_url;
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });


  // Обработчик для формы регистрации
  const signupForm = document.getElementById('signup-form');
  signupForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const signupData = {
      first_name: document.getElementById('signup-first-name').value,
      last_name: document.getElementById('signup-second-name').value,
      patronymic: document.getElementById('signup-patronymic').value,
      email: document.getElementById('signup-email').value,
      password: document.getElementById('signup-password').value,
      password_repeat: document.getElementById('signup-password-repeat').value
    };

    console.log(signupData)

    fetch('/signup/', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(signupData),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert(data.message);
        window.location.href = data.redirect_url;
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
});

