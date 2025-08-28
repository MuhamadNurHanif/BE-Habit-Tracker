# BE-Habit-Tracker
Techstack: django-ninja


# Struktur Direktori
BE-Habit-Tracker/           # Root project
├── habit_tracker/          # Folder "utama" project (setting Django)
│   ├── settings.py         # Konfigurasi project (database, apps, dll)
│   ├── urls.py             # Routing utama
│   ├── asgi.py / wsgi.py   # Entry point server (abaikan dulu)
│
├── habits/                 # App khusus untuk Habit + HabitLog
│   ├── models.py           # Tempat bikin schema tabel DB (pakai Django ORM)
│   ├── schemas.py          # Tempat bikin schema Pydantic (buat Django Ninja API)
│   ├── views.py            # Tempat bikin endpoint REST API
│   ├── urls.py             # Routing khusus app habits
│
├── users/                  # App khusus user
│   ├── models.py           # Kalau mau extend User bawaan Django
│   ├── schemas.py          # Schema Pydantic untuk API user
│   ├── views.py            # Endpoint user
│   ├── urls.py             # Routing khusus user
│
├── manage.py               # Command line Django (jalankan project, migrate, dll)
├── venv/                   # Virtual environment Python
└── README.md               # Dokumentasi