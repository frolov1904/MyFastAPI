# MyFastAPI

Учебный backend-проект на **FastAPI** для управления студентами и специальностями.

Проект развивался поэтапно: от простого API с хранением данных в JSON до полноценного приложения с PostgreSQL, миграциями, авторизацией, ролями, автоматическими тестами и простым веб-интерфейсом.

## Описание проекта

MyFastAPI — это система управления студентами, реализованная на FastAPI.

Проект включает:

* REST API для работы со студентами и специальностями;
* PostgreSQL в качестве основной базы данных;
* миграции базы данных через Alembic;
* DAO-слой для работы с данными;
* регистрацию и авторизацию пользователей;
* JWT-аутентификацию через cookie;
* ролевую модель доступа;
* автоматические тесты на pytest;
* простой UI-интерфейс для работы с системой.

## Основная функциональность

### Студенты

* получение списка студентов;
* добавление студента;
* обновление данных студента;
* удаление студента;
* привязка студента к специальности.

### Специальности

* получение списка специальностей;
* добавление специальности;
* связь специальности со студентами.

### Пользователи и авторизация

* регистрация пользователя;
* вход пользователя;
* выход пользователя;
* получение текущего пользователя;
* хранение пароля только в виде хеша;
* JWT-токен в cookie;
* роли пользователей.

### Роли и права доступа

В проекте реализована базовая ролевая модель:

* обычный пользователь может просматривать данные, добавлять и обновлять студентов;
* администратор может добавлять специальности и удалять студентов;
* недоступные действия скрываются в UI, но дополнительно защищены на backend-уровне.

## Технологический стек

* Python
* FastAPI
* Uvicorn
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Pydantic Settings
* JWT / python-jose
* Passlib / bcrypt
* Pytest
* Pytest-asyncio
* HTTPX
* Jinja2
* HTML / CSS / JavaScript
* Docker Compose
* Adminer

## Структура проекта

```text
MyFastAPI/
├── app/
│   ├── dao/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── migration/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── pages/
│   │   ├── __init__.py
│   │   └── router.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── ui.js
│   ├── students/
│   │   ├── __init__.py
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── login.html
│   ├── users/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dao.py
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_students.py
│   └── test_ui.py
├── alembic.ini
├── docker-compose.yml
├── pytest.ini
├── req.txt
├── CHANGELOG.md
└── README.md
```

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/frolov1904/MyFastAPI.git
cd MyFastAPI
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 3. Активировать виртуальное окружение

Для macOS / Linux:

```bash
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### 4. Установить зависимости

```bash
pip install -r req.txt
```

### 5. Создать файл `.env`

В корне проекта нужно создать файл `.env`.

Пример содержимого:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=myfastapi
DB_USER=postgres
DB_PASSWORD=postgres

SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

Секретный ключ можно сгенерировать командой:

```bash
openssl rand -hex 32
```

Файл `.env` не должен попадать в Git.

### 6. Запустить PostgreSQL и Adminer

```bash
docker compose up -d
```

После запуска будут доступны:

* PostgreSQL на порту `5433`;
* Adminer по адресу `http://localhost:8080`.

Данные для входа в Adminer:

```text
System: PostgreSQL
Server: postgres
Username: postgres
Password: postgres
Database: myfastapi
```

### 7. Применить миграции

```bash
alembic upgrade head
```

### 8. Запустить приложение

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

## Основные страницы

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger используется как техническая документация API.

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

### UI входа

```text
http://127.0.0.1:8000/ui/login
```

### Панель управления

```text
http://127.0.0.1:8000/ui
```

В панели управления отображаются только те действия, которые доступны текущему пользователю по его роли.

## API-эндпоинты

### Авторизация

```http
POST /auth/register
POST /auth/login
GET /auth/me
POST /auth/logout
```

### Студенты

```http
GET /students
POST /students
PUT /students/{student_id}
DELETE /students/{student_id}
```

### Специальности

```http
GET /majors
POST /majors
```

## Примеры запросов

### Регистрация пользователя

```http
POST /auth/register
```

```json
{
  "email": "alex@example.com",
  "password": "123456",
  "phone_number": "+79991234567",
  "first_name": "Алексей",
  "last_name": "Фролов"
}
```

### Вход пользователя

```http
POST /auth/login
```

```json
{
  "email": "alex@example.com",
  "password": "123456"
}
```

После успешного входа сервер создаёт JWT-токен и сохраняет его в cookie `users_access_token`.

### Получение текущего пользователя

```http
GET /auth/me
```

### Создание специальности

Доступно только администратору.

```http
POST /majors
```

```json
{
  "major_name": "Информатика",
  "major_description": "Направление, связанное с программированием и информационными технологиями"
}
```

### Создание студента

Доступно авторизованному пользователю.

```http
POST /students
```

```json
{
  "phone_number": "+79991234567",
  "first_name": "Иван",
  "last_name": "Иванов",
  "date_of_birth": "2002-04-10",
  "email": "ivan@example.com",
  "address": "г. Москва, ул. Тестовая, д. 1",
  "enrollment_year": 2022,
  "course": 2,
  "special_notes": "Тестовый студент",
  "major_id": 1
}
```

### Обновление студента

Доступно авторизованному пользователю.

```http
PUT /students/{student_id}
```

```json
{
  "course": 3,
  "major_id": 1
}
```

### Удаление студента

Доступно только администратору.

```http
DELETE /students/{student_id}
```

## Ролевая модель

В таблице пользователей предусмотрены роли:

```text
is_user
is_student
is_teacher
is_admin
is_super_admin
```

На текущем этапе активно используются:

* `is_user`;
* `is_admin`;
* `is_super_admin`.

Обычный пользователь может добавлять и обновлять студентов.

Администратор может добавлять специальности и удалять студентов.

Чтобы вручную выдать пользователю роль администратора в локальной БД, можно выполнить:

```bash
docker exec -it myfastapi_postgres psql -U postgres -d myfastapi -P pager=off -c "UPDATE users SET is_admin = true WHERE email = 'alex@example.com';"
```

## Тестирование

Для тестов используется отдельная база данных:

```text
myfastapi_test
```

Создать тестовую базу можно командой:

```bash
docker exec -it myfastapi_postgres psql -U postgres -c "CREATE DATABASE myfastapi_test;"
```

Запуск всех тестов:

```bash
pytest -v
```

В проекте есть тесты:

* регистрации пользователя;
* входа пользователя;
* получения текущего пользователя;
* выхода пользователя;
* проверки ролей;
* работы со студентами;
* работы со специальностями;
* доступности UI-страниц;
* доступности статических CSS и JS-файлов.

## Миграции

Создание новой миграции:

```bash
alembic revision --autogenerate -m "migration name"
```

Применение миграций:

```bash
alembic upgrade head
```

Просмотр текущей миграции:

```bash
alembic current
```

История миграций:

```bash
alembic history
```

## Docker Compose

В проекте через Docker Compose поднимаются:

* PostgreSQL;
* Adminer.

Запуск:

```bash
docker compose up -d
```

Остановка:

```bash
docker compose down
```

Остановка с удалением volume:

```bash
docker compose down -v
```

## Этапы развития проекта

Проект развивался по версиям:

* `0.1.0` — базовый FastAPI API и чтение данных из JSON;
* `0.2.0` — CRUD-операции и Pydantic-схемы;
* `0.3.0` — PostgreSQL, SQLAlchemy и Alembic;
* `0.4.0` — DAO-слой и переход API с JSON на PostgreSQL;
* `0.5.0` — пользователи, JWT-аутентификация и роли;
* `0.6.0` — автоматические тесты;
* `0.7.0` — простой UI-интерфейс и ролевая веб-панель.

Подробности по версиям находятся в `CHANGELOG.md`.

## Текущее состояние

На текущем этапе проект можно считать завершённым как учебный backend-проект.

Реализованы:

* backend на FastAPI;
* PostgreSQL;
* миграции;
* авторизация;
* роли;
* тесты;
* простой веб-интерфейс.

Возможные будущие улучшения:

* Dockerfile для запуска FastAPI-приложения в контейнере;
* CI/CD pipeline;
* пагинация и фильтрация студентов;
* более подробная система ролей;
* улучшение UI;
* расширение тестового покрытия.
