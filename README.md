## FoodGram
- Проект FoodGram - сайт с рецептами блюд, можно добавлять свои рецепты а так же скачивать уже готовые..

### Готовый пользователь от сайта и админ-панели
- адрес http://51.250.101.211/
- 1@1.ru почта
- 1 пароль(просто единичка)

##### Технологии:
- Nginx
- Gunicorn
- Django REST
- Docker
- Postgres

##### Запуск проекта:
- Запустить ваш Docker
- Перейти в папку ./infra
- Выполнить команду:
[[[docker-compose up -d --build --force-recreate]]]
- ✨Magic ✨(Сервис запустится в фоновом режиме)
- Сделать миграции:
[[[docker-compose exec backend python manage.py migrate]]]
- Загрузить тестовые данные:
[[[docker-compose exec backend python manage.py loaddata 1.json]]]
- Тестовый супер-пользователь уже есть:
[[[1@1.ru - email;
1 - password;]]]
- Создание своего супер-пользователя:
docker-compose exec backend python manage.py createsuperuser

#### Автор
- george20211