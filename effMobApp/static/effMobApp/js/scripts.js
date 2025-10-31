// Функция для извлечения csrftoken'а
function getCSRFToken() {
  const cookieName = 'csrftoken=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookies = decodedCookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return '';
}

// Функция для отправки POST-запроса

function sendPostRequest(url, onSuccess) {
  const csrfToken = getCSRFToken();

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    credentials: 'include'
  })
  .then(async (response) => {
    // Пытаемся всегда распарсить JSON
    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error('Некорректный ответ сервера (ожидался JSON)');
    }

    // Проверяем статус запроса
    if (!response.ok) {
      // Если сервер вернул ошибку (4xx/5xx), бросаем исключение
      const message = data.message || `Ошибка ${response.status}`;
      throw new Error(message);
    }

    // Всё ок — возвращаем JSON
    return data;
  })
  .then((data) => {
    // Обработка успешного JSON-ответа
    if (data.status === 'success') {
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else if (typeof onSuccess === 'function') {
        onSuccess(data);
      }
    } else {
      alert(data.message || 'Ошибка запроса');
    }
  })
  .catch((error) => {
    console.error('Ошибка:', error);
    alert(error.message || 'Ошибка сети');
  });
}

// function sendPostRequest(url, onSuccess) {
//     const csrfToken = getCSRFToken();

//     fetch(url, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': csrfToken
//       },
//       credentials: 'include'
//     })
//     .then(response => {
//       // Если ожидаем JSON
//       if (response.headers.get('content-type')?.includes('application/json')) {
//         return response.json();
//       }
//       // Если пришёл HTML
//       return { status: response.ok ? 'success' : 'error', redirect_url: response.url };
//     })
//     .then(data => {
//       if (data.status === 'success') {
//         // Если есть redirect_url — идём туда
//         if (data.redirect_url) {
//           window.location.href = data.redirect_url;
//         } else if (typeof onSuccess === 'function') {
//           onSuccess(data);
//         }
//       } else {
//         alert(data.message || 'Ошибка запроса');
//       }
//     })
//     .catch(error => {
//       console.error('Ошибка:', error);
//     });
//   }

  // Функция прослушки кликов по кнопке
  function bindButton(id, endpoint) {
    const button = document.getElementById(id);
    if (!button) return;

    button.addEventListener('click', function(event) {
      event.preventDefault();
      sendPostRequest(endpoint);
    });
  }