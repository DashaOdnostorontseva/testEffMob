document.addEventListener('DOMContentLoaded', function() {

    const csrfToken = getCSRFToken();

    fetch('editProfile/', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
        const user = data.user;
        document.getElementById('upd-email').value = user.email || '';
        document.getElementById('upd-first-name').value = user.first_name || '';
        document.getElementById('upd-last-name').value = user.last_name || '';
        document.getElementById('upd-patronymic').value = user.patronymic || '';
        } else {
        alert(data.message);
        }
    })
    .catch(error => console.error('Ошибка загрузки профиля:', error));
  
    const updateProfileForm = document.getElementById('edit-form');
    updateProfileForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const updData = {
            first_name: document.getElementById('upd-first-name').value,
            last_name: document.getElementById('upd-last-name').value,
            patronymic: document.getElementById('upd-patronymic').value,
            email: document.getElementById('upd-email').value,
            password: document.getElementById('upd-password').value,
            password_repeat: document.getElementById('upd-repeat-password').value
        };
        fetch('updateProfileData/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(updData),
            credentials: 'include'
        })
        .then(response => response.json())
            .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect_url;
            } else if (data.status === 'error') {
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error('Ошибка:', error);
        });
    });
})