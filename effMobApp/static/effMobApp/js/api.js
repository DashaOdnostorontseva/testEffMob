document.addEventListener('DOMContentLoaded', function() {
  const button = document.getElementById('get-users-data-button');
  const tableBody = document.querySelector('#users-table tbody');
  button.addEventListener('click', function(event) {
    event.preventDefault();
    const csrfToken = getCSRFToken();

    fetch('api/users/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        console.log('Данные пользователей:', data.data);
        tableBody.innerHTML = '';
        if (data.data.length > 0) {
            document.getElementById('users-table').hidden = false;
        } else {
            document.getElementById('users-table').hidden = true;
            alert('Нет пользователей для отображения');
        }
        data.data.forEach(user => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.first_name || ''}</td>
            <td>${user.last_name || ''}</td>
            <td>${user.email}</td>
            <td>
              <select data-user-id="${user.id}">
                <option value="user" ${user.role_type === 'user' ? 'selected' : ''}>user</option>
                <option value="operator" ${user.role_type === 'operator' ? 'selected' : ''}>operator</option>
                <option value="admin" ${user.role_type === 'admin' ? 'selected' : ''}>admin</option>
              </select>
            </td>
          `;
          tableBody.appendChild(row);
        });

        attachSelectListeners();
      } else {
        alert(`Ошибка: ${data.message}`);
      }
    })
    .catch(error => console.error('Ошибка запроса:', error));
  });

    function attachSelectListeners() {
        document.querySelectorAll('select[data-user-id]').forEach(select => {
        select.addEventListener('change', function() {
            const newRole = this.value;
            const userId = this.dataset.userId;
            updateUserRole(userId, newRole);
            });
        });
    }

    function updateUserRole(userId, newRole) {
        const csrfToken = getCSRFToken();

        fetch(`api/update_role/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        body: JSON.stringify({
            user_id: userId,
            role_type: newRole
        })
        })
        .then(response => response.json())
        .then(data => {
        if (data.status === 'success') {
            alert(`Роль пользователя ${userId} обновлена на ${newRole}`);
        } else {
            alert(`Ошибка: ${data.message}`);
        }
        })
        .catch(error => console.error('Ошибка при обновлении роли:', error));
    }
});