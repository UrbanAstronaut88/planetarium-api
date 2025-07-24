# 🌌 Planetarium API

A REST API for a ticket booking system for astronomical shows in a planetarium.

## 📦 Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose


## 🚀 Features

- Management of planetarium domes
- Creating and viewing astronomy shows
- Show themes
- Creating show schedules (sessions)
- Booking tickets (Reservations)
- Viewing available seats for sessions
- JWT authentication

## 🔧 Installation and Launch (without Docker)

### 1. Clone the repository:

```bash
git clone https://github.com/urbanastronaut88/planetarium-api.git
cd planetarium-api
```

### 2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply migrations:
```bash
python manage.py migrate
```

### 5.Run the development server:
```bash
python manage.py runserver
```
The API will be available at:
http://127.0.0.1:8000/

## 🐳 Run with Docker

### If you prefer to run the project in containers:
```bash
docker-compose up --build
```

#### Tests:
```bash
manage.py test planetarium.tests.test_views
```