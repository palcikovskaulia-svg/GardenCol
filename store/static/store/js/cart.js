// =========================================================
// 1. ФУНКЦІЯ ОТРИМАННЯ CSRF ТОКЕНА (ПОВИННА БУТИ В ГЛОБАЛЬНІЙ ОБЛАСТІ)
// =========================================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// =========================================================
// 2. ФУНКЦІЯ ОБРОБКИ AJAX ЗАПИТУ
// =========================================================
function updateUserOrder(productId, action){
    console.log('User is GUEST. Sending data...')

    var url = '/update_item/'

    // Отримуємо токен
    const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            // ВИПРАВЛЕННЯ: Додаємо CSRF-токен до заголовків
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       // Перевіряємо, чи відповідь успішна
       if (!response.ok) {
           console.error("Помилка відповіді сервера:", response.status);
           // Якщо це 403 Forbidden, це 100% проблема з токеном
           return Promise.reject(`Server error: ${response.status}`);
       }
       // Якщо відповідь успішна, очікуємо JSON
       return response.json();
    })
    .then((data) => {
        console.log('data:', data)
        // Перезавантажуємо сторінку, щоб оновити дані
        location.reload()
    })
    .catch(error => {
        console.error('Помилка AJAX:', error);
        alert("Помилка при додаванні товару. Перевірте консоль (F12)!");
    });
}


// =========================================================
// 3. ОБРОБНИК ПОДІЙ КНОПОК
// =========================================================
// Цей код запускається, коли DOM завантажено
var updateBtns = document.getElementsByClassName('update-cart')

// Уникайте використання "var i", оскільки це може створити глобальну змінну,
// краще використовувати let або forEach, але цикл for з 'var' працює
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        updateUserOrder(productId, action)
    })
}