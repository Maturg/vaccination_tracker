# Kittygram API

REST API для управления котиками и их достижениями. Проект написан на Django REST Framework, контейнеризирован с помощью Docker.

## Функционал

- Регистрация и аутентификация пользователей (токены)
- CRUD операции для котиков
- Управление достижениями котиков
- Пагинация (10 объектов на страницу)
- Поиск и фильтрация котиков
- Документация API (Swagger/ReDoc)

## Стек технологий

- Python 3.10
- Django 3.2.25
- Django REST Framework 3.14.0
- Djoser (аутентификация)
- Gunicorn (WSGI-сервер)
- Docker / Docker Compose

## Зависимости

Все зависимости перечислены в файле `requirements.txt`:

```
Django==3.2.25
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
djoser==2.1.0
django-cors-headers==3.13.0
python-dotenv==1.0.0
Pillow==10.1.0
gunicorn==20.1.0
drf-yasg==1.21.7
```

## Установка и запуск (локально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/Maturg/kittygram.git
cd kittygram
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните при необходимости:

```bash
cp .env.example .env
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

## Запуск через Docker

### 1. Сборка образа

```bash
docker build -t kittygram_backend .
```

### 2. Запуск контейнера

```bash
docker run -p 8000:8000 kittygram_backend
```

### 3. Или через Docker Compose

```bash
docker-compose up --build
```