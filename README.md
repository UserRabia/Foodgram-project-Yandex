# Foodgram

"Foodgram" - это веб-приложение, где пользователи могут делиться и находить рецепты, добавлять их в избранное, подписываться на других авторов и создавать список покупок для ингредиентов, необходимых для приготовления выбранных блюд.

## Возможности

- **Аутентификация пользователя:** Пользователи могут регистрироваться, входить в систему и управлять своими профилями.
- **Управление рецептами:** Пользователи могут публиковать, редактировать и удалять свои рецепты.
- **Избранное:** Пользователи могут добавлять рецепты в избранное.
- **Подписки:** Пользователи могут подписываться на других авторов, чтобы получать обновления о их рецептах.
- **Список покупок:** Пользователи могут создавать список покупок с ингредиентами, необходимыми для выбранных рецептов.

## Используемые технологии

- **Backend:**
  - Python
  - Django
  - Django Rest Framework
  - PostgreSQL

- **Frontend:**
  - React

- **Инфраструктура:**
  - Docker

- **Облачные сервисы:**
  - Yandex Cloud

## Начало работы

Чтобы запустить приложение Foodgram локально, выполните следующие шаги:

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com/ваш-логин/foodgram.git
   cd foodgram

2. **Настроить переменные окружения:**
Создайте файл .env в корне проекта и настройте необходимые переменные окружения.

3. **Создать и запустить Docker Compose:**
    ```bash
    docker-compose up --build
4. **Применить миграции:**
    ```bash
    docker-compose exec backend python manage.py migrate
5. **Создать суперпользователя (администратора):**
    ```bash
    docker-compose exec backend python manage.py createsuperuser
6. **Доступ к приложению:**
Откройте ваш веб-браузер и перейдите по адресу http://localhost:8000.

7. **Доступ к админ-панели:**
Войдите с учетными данными суперпользователя по адресу http://localhost:8000/admin.

## Использование
- **Регистрация пользователя:**
    - Зарегистрируйте новый аккаунт на сайте.

- **Управление рецептами:**
    - Войдите в свой аккаунт, чтобы публиковать, редактировать или удалять свои рецепты.

- **Избранное и Подписки:**
    - Исследуйте рецепты от других авторов и добавляйте их в избранное.
    - Подписывайтесь на авторов, чтобы получать обновления о их последних рецептах.

- **Список покупок:**
    - Создавайте список покупок, добавляя ингредиенты из выбранных рецептов.

## Автор 
### [Амачиева Рабия](https://github.com/UserRabia)
