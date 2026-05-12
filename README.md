# Vaccination Tracker API

REST API для отслеживания вакцинаций домашних питомцев. Проект написан на Django REST Framework, контейнеризирован с помощью Docker.

## Функционал

- Управление питомцами (CRUD)
- Справочник вакцин (CRUD)
- Добавление записей о вакцинациях с автоматическим расчётом даты следующей
- Просмотр просроченных вакцинаций
- Просмотр предстоящих вакцинаций (следующие 30 дней)
- История вакцинаций конкретного питомца
- Фильтрация вакцинаций по вакцине
- Аутентификация по токенам (Djoser)
- Права доступа: владелец может изменять только своих питомцев

## Стек технологий

- Python 3.10
- Django 3.2.25
- Django REST Framework 3.14.0
- Djoser (аутентификация)
- Gunicorn (WSGI-сервер)
- Whitenoise (раздача статики)
- Docker / Docker Compose
- SQLite (разработка)

## Зависимости

```
Django==3.2.25
djangorestframework==3.14.0
djangorestframework-simplejwt==4.8.0
djoser==2.1.0
django-cors-headers==3.13.0
python-dotenv==1.0.0
gunicorn==20.1.0
django-filter==23.1
whitenoise==6.6.0
```

## Установка и запуск (локально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/ВАШ_АККАУНТ/vaccination_tracker.git
cd vaccination_tracker
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/macOS
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

## Запуск через Docker

```bash
docker-compose up --build
```

## API Эндпоинты

| Метод     | URL                               | Описание              | Права |
| GET       | `/api/cats/`                      | Список питомцев       | все |
| POST      | `/api/cats/`                      | Создать питомца       | авторизованные |
| PUT/PATCH | `/api/cats/{id}/`                 | Изменить питомца      | владелец |
| DELETE    | `/api/cats/{id}/`                 | Удалить питомца       | владелец |
| GET       | `/api/vaccines/`                  | Список вакцин         | все |
| POST      | `/api/vaccines/`                  | Создать вакцину       | только админ |
| PUT/PATCH | `/api/vaccines/{id}/`             | Изменить вакцину      | только админ |
| DELETE    | `/api/vaccines/{id}/`             | Удалить вакцину       | только админ |
| GET       | `/api/vaccinations/`              | Список вакцинаций     | все |
| POST      | `/api/vaccinations/`              | Добавить вакцинацию   | авторизованные |
| GET       | `/api/vaccinations/overdue/`      | Просроченные          | все |
| GET       | `/api/vaccinations/upcoming/`     | Предстоящие (30 дней) | все |
| GET       | `/api/vaccinations/?vaccine={id}` | Фильтр по вакцине     | все |
| GET       | `/api/vaccinations/{id}/history/` | История питомца       | все |

## Примеры запросов

### Регистрация пользователя

```bash
curl -X POST http://127.0.0.1:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "UserPass123", "email": "user@mail.com"}'
```

### Получение токена

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "UserPass123"}'
```

### Создание питомца

```bash
curl -X POST http://127.0.0.1:8000/api/cats/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{"name": "Барсик", "color": "White", "birth_year": 2020}'
```

### Добавление вакцинации

```bash
curl -X POST http://127.0.0.1:8000/api/vaccinations/ \
  -H "Authorization: Token ваш_токен" \
  -H "Content-Type: application/json" \
  -d '{"cat": 1, "vaccine": 1, "vaccination_date": "2025-05-01"}'
```

### Просмотр просроченных вакцинаций

```bash
curl -X GET http://127.0.0.1:8000/api/vaccinations/overdue/ \
  -H "Authorization: Token ваш_токен"
```
