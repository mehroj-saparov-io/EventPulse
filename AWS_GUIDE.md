# 🚀 1. Serverga tayyorlash (bir martalik)

SSH orqali kirganingizdan so‘ng:

```bash
sudo apt update
sudo apt upgrade -y
```

Kerakli paketlarni o‘rnating:

```bash
sudo apt install python3-pip python3-venv nginx git -y
```

---

# 📦 2. Loyihani serverga olish

```bash
git clone https://github.com/mehroj-saparov-io/EventPulse.git
cd eventpulse
```

---

# 🐍 3. Virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

# 🔑 4. .env fayl yaratish

```bash
nano .env
```

Ichiga quyidagilarni yozing:

```env
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:pass@127.0.0.1:5432/dbname
```

---

# 🗄 5. PostgreSQL o‘rnatish

```bash
sudo apt install postgresql postgresql-contrib -y
```

Keyin:

```bash
sudo -u postgres psql
```

Ichida:

```sql
CREATE DATABASE eventpulse_db;
CREATE USER eventpulse_user WITH PASSWORD 'password';
ALTER ROLE eventpulse_user SET client_encoding TO 'utf8';
ALTER ROLE eventpulse_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventpulse_db TO eventpulse_user;
```

---

# ⚙️ 6. Django setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Static fayllar:

```bash
python manage.py collectstatic
```

Test uchun:

```bash
python manage.py runserver 0.0.0.0:8000
```

Brauzerda tekshiring:

```
http://SERVER_IP:8000
```

Agar ishlayotgan bo‘lsa, keyingi bosqichga o‘ting.

---

# 🔥 7. Gunicorn (production server)

O‘rnatish:

```bash
pip install gunicorn
```

Test:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

# ⚙️ 8. systemd service (MUHIM)

```bash
sudo nano /etc/systemd/system/eventpulse.service
```

Ichiga quyidagini yozing:

```ini
[Unit]
Description=EventPulse Gunicorn Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/eventpulse
ExecStart=/home/ubuntu/eventpulse/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/eventpulse/eventpulse.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Keyin:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start eventpulse
sudo systemctl enable eventpulse
```

Holatini tekshiring:

```bash
sudo systemctl status eventpulse
```

---

# 🌐 9. Nginx sozlash

```bash
sudo nano /etc/nginx/sites-available/eventpulse
```

Ichiga quyidagini yozing:

```nginx
server {
    listen 80;
    server_name YOUR_SERVER_IP;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ubuntu/eventpulse;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/eventpulse/eventpulse.sock;
    }
}
```

Faollashtiring:

```bash
sudo ln -s /etc/nginx/sites-available/eventpulse /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

# ✅ 10. TEST

Brauzerda oching:

```
http://SERVER_IP
```

---
