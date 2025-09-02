# BE-Habit-Tracker

Backend untuk aplikasi **Habit Tracker** menggunakan **Django + Django-Ninja** dengan database PostgreSQL.  
Berfungsi sebagai REST API untuk mendukung CRUD habit/todo di frontend (React + Vite).

---

## Tech Stack

- **Framework**: Django 5.2.5
- **API**: Django-Ninja
- **Database**: PostgreSQL
- **ORM**: Django ORM

---

## Struktur Direktori

```bash
BE-Habit-Tracker/
├── habit_tracker/
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│
├── habits/
│ ├── models.py
│ ├── schemas.py
│ ├── views.py
│ ├── urls.py
├── manage.py
├── venv/
└── README.md
```

---

## Endpoints

```bash
GET http://127.0.0.1:8000/api/todos/ → list todo
POST http://127.0.0.1:8000/api/todos/ → create todo
GET http://127.0.0.1:8000/api/todos/{id} → detail
PUT http://127.0.0.1:8000/api/todos/{id} → update
DELETE http://127.0.0.1:8000/api/todos/{id} → delete
```

---

## Cara Menjalankan

```bash
git clone https://github.com/username/BE-Habit-Tracker.git
cd BE-Habit-Tracker
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
