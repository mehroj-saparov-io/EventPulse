# 🚀 EventPulse – Event Management Backend API

## 📌 Project Overview

**EventPulse** — bu online va offline eventlarni boshqarish uchun ishlab chiqilgan REST API.
Foydalanuvchilar eventlarga ro‘yxatdan o‘tishi, adminlar esa event yaratishi va statistikani kuzatishi mumkin.

Loyiha **Django REST Framework** asosida yozilgan va **production-ready deployment** uchun tayyorlangan.

---

## ⚙️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** PostgreSQL
* **Environment Config:** django-environ
* **Server:** Gunicorn
* **Reverse Proxy:** Nginx
* **Deployment:** AWS EC2 (Ubuntu 22.04)
* **Process Manager:** systemd
* **Version Control:** Git, GitHub

---

## 🔐 Authentication & Authorization

* Custom User model ishlatilgan
* JWT (Access + Refresh token)
* Protected endpointlar token talab qiladi
* Admin-only endpointlar mavjud

---

## 📦 Features

### 👤 Users

* Register (`/api/users/register/`)
* Login (`/api/users/login/`)
* Current user (`/api/users/me/`)

---

### 📅 Events

Event modeli:

* title
* description
* event_type (ONLINE / OFFLINE)
* location (faqat OFFLINE uchun)
* start_time
* end_time
* capacity
* created_by

#### Business Rules:

* `end_time < start_time` → validation error
* Offline event → location majburiy
* `capacity = 0` → registration yopiladi

#### Endpointlar:

* `GET /api/events/`
* `GET /api/events/<id>/`
* `POST /api/events/create/` (Admin only)
* `PUT /api/events/<id>/update/` (Admin only)
* `DELETE /api/events/<id>/delete/` (Admin only)

---

### 🎟 Event Registration (Core Logic)

Bu loyiha ichidagi **eng muhim qism**.

#### Qoidalar:

* Foydalanuvchi **bitta eventga faqat 1 marta** ro‘yxatdan o‘tadi
* Event capacity oshib ketmaydi
* Registration cancel qilish mumkin
* Alohida `Registration` modeli mavjud

#### Status:

* REGISTERED
* CANCELLED

#### Endpointlar:

* `POST /api/registrations/register/`
* `PUT /api/registrations/cancel/<id>/`

---

### 📊 Statistics (Admin only)

* Eventdagi ro‘yxatdan o‘tganlar soni
* Bo‘sh joylar soni
* Eng mashhur eventlar (Top 5)

#### Endpoint:

* `GET /api/registrations/stats/`

---

## 🧠 Business Logic Summary

* Event to‘lsa → yangi registration qabul qilinmaydi
* User duplicate registration qila olmaydi
* Cancel qilinganda joy bo‘shaydi
* Offline event → location majburiy

---

## 🔑 Environment Variables

Loyiha `django-environ` orqali boshqariladi.

`.env` fayl namunasi:

```env
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:pass@127.0.0.1:5432/dbname
```

❗ `.env` fayl GitHub’ga yuklanmaydi

---

## ⚙️ Local Setup

```bash
# Clone project
git clone https://github.com/your-username/eventpulse.git
cd eventpulse

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Environment file
cp .env.example .env

# Migrations
python manage.py makemigrations
python manage.py migrate

# Superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🌐 Deployment (AWS EC2)

1. EC2 instance yaratish (Ubuntu 22.04)
2. SSH orqali ulanish
3. Python, PostgreSQL, Gunicorn o‘rnatish
4. `.env` sozlash (`DEBUG=False`)
5. Gunicorn service yaratish (systemd)
6. Nginx reverse proxy sozlash
7. Static files serve qilish

---

## 🔒 Security

* `DEBUG=False`
* `ALLOWED_HOSTS` sozlangan
* JWT authentication ishlatilgan
* `.env` orqali secretlar yashirilgan
* Database tashqi kirishdan himoyalangan

---

## 🧪 Testing

* Postman orqali barcha endpointlar test qilingan
* Registration logic (duplicate + capacity) tekshirilgan
* Admin-only endpointlar verifikatsiya qilingan

---

## 📁 Project Structure

```
apps/
 ├── users/
 ├── events/
 ├── registrations/

config/
 ├── settings.py
 ├── urls.py
```

---

## 👨‍💻 Author

* Backend Developer: Mehroj Saparov
* GitHub: https://github.com/mehroj-saparov-io
