document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login-btn');
  const tokenDisplay = document.getElementById('token-display');
  const apiSection = document.getElementById('api-section');
  const loadBtn = document.getElementById('load-users');
  const table = document.getElementById('users-table');
  const tableBody = table.querySelector('tbody');

  loginBtn.addEventListener('click', () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/api/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.access) {
        localStorage.setItem('accessToken', data.access);
        tokenDisplay.textContent = 'Токен получен и сохранен';
        apiSection.hidden = false;
      } else {
        tokenDisplay.textContent = 'Ошибка авторизации';
      }
    })
    .catch(err => console.error('Ошибка логина:', err));
  });

  loadBtn.addEventListener('click', () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('Сначала войдите и получите токен');
      return;
    }

    fetch('/external/users/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        table.hidden = false;
        tableBody.innerHTML = '';
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
        alert(data.message);
      }
    })
    .catch(err => console.error('Ошибка загрузки пользователей:', err));
  });

  function attachSelectListeners() {
    document.querySelectorAll('select[data-user-id]').forEach(select => {
      select.addEventListener('change', function() {
        const newRole = this.value;
        const userId = this.dataset.userId;
        updateRole(userId, newRole);
      });
    });
  }

  function updateRole(userId, newRole) {
    const token = localStorage.getItem('accessToken');
    fetch('/external/update_role/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ user_id: userId, role_type: newRole })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        alert(`Роль пользователя ${userId} изменена на ${newRole}`);
      } else {
        alert(`Ошибка: ${data.message}`);
      }
    })
    .catch(err => console.error('Ошибка обновления роли:', err));
  }
});
