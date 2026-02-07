# Server Setup Commands

Serverda quyidagi buyruqlarni ketma-ket bajaring:

## 1. Hozirgi holatni tekshirish

```bash
cd /var/www/Crmtizim
ls -la gunicorn.sock
cat .env
```

## 2. .env faylini yaratish/yangilash

```bash
nano /var/www/Crmtizim/.env
```

Quyidagini kiriting:

```env
DEBUG=False
SECRET_KEY=django-insecure-change-this-in-production-to-random-string
ALLOWED_HOSTS=13.39.83.160,localhost,127.0.0.1
USE_POSTGRES=True
DB_NAME=crmtizim_db
DB_USER=crmtizim_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
```

Ctrl+O → Enter → Ctrl+X

## 3. Nginx konfiguratsiyasini tekshirish

```bash
cat /etc/nginx/sites-available/crmtizim
```

Agar noto'g'ri bo'lsa, to'g'irlang:

```bash
sudo nano /etc/nginx/sites-available/crmtizim
```

To'g'ri konfiguratsiya:

```nginx
server {
    listen 80;
    server_name 13.39.83.160;

    client_max_body_size 10M;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias /var/www/Crmtizim/staticfiles/;
    }

    location /media/ {
        alias /var/www/Crmtizim/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Crmtizim/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

## 4. Gunicorn service faylini tekshirish

```bash
cat /etc/systemd/system/gunicorn.service
```

To'g'ri konfiguratsiya:

```ini
[Unit]
Description=Gunicorn daemon for Crmtizim
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/Crmtizim
Environment="PATH=/var/www/Crmtizim/venv/bin"
ExecStart=/var/www/Crmtizim/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/Crmtizim/gunicorn.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

## 5. Ruxsatlarni to'g'rilash

```bash
sudo chown -R ubuntu:www-data /var/www/Crmtizim
sudo chmod -R 755 /var/www/Crmtizim
```

## 6. Xizmatlarni qayta ishga tushirish

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 7. Statusni tekshirish

```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
ls -la /var/www/Crmtizim/gunicorn.sock
```

## 8. Xatoliklarni ko'rish (agar kerak bo'lsa)

```bash
sudo journalctl -u gunicorn -n 100 --no-pager
sudo tail -n 50 /var/log/nginx/error.log
```

## 9. AWS Security Group tekshirish

AWS konsolida:
- EC2 → Security Groups → Inbound Rules
- Port 80 (HTTP) ochiq bo'lishi kerak: `0.0.0.0/0`

## 10. Saytni ochib ko'rish

Brauzerda: `http://13.39.83.160`
