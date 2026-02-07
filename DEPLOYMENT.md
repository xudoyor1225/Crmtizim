# 🚀 Server Deployment Guide

## 📋 Server Talablari

- **OS:** Ubuntu 22.04 LTS (yoki yangi)
- **Python:** 3.12+
- **PostgreSQL:** 13+
- **Nginx:** Latest
- **Redis:** 6+ (Celery uchun)
- **RAM:** Minimal 2GB (tavsiya: 4GB)
- **Disk:** 20GB+

---

## 1️⃣ Server Tayyorlash

### Sistemani yangilash
```bash
sudo apt update && sudo apt upgrade -y
```

### Kerakli paketlarni o'rnatish
```bash
sudo apt install -y python3.12 python3.12-venv python3-pip \
    postgresql postgresql-contrib nginx redis-server \
    git curl wget build-essential libpq-dev
```

---

## 2️⃣ PostgreSQL Sozlash

### Baza va foydalanuvchi yaratish
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE crmtizim_db;
CREATE USER crmtizim_user WITH PASSWORD 'your_secure_password_here';
ALTER ROLE crmtizim_user SET client_encoding TO 'utf8';
ALTER ROLE crmtizim_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crmtizim_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE crmtizim_db TO crmtizim_user;

-- PostgreSQL 15+ uchun
\c crmtizim_db
GRANT ALL ON SCHEMA public TO crmtizim_user;
\q
```

---

## 3️⃣ Loyihani Clone Qilish

### Clone
```bash
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/Crmtizim.git
sudo chown -R $USER:$USER Crmtizim
cd Crmtizim
```

### Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```

### Dependencies
```bash
pip install --upgrade pip
pip install -r requirements/base.txt
pip install gunicorn
```

---

## 4️⃣ Environment Sozlash

### .env fayl yaratish
```bash
cp .env.example .env
nano .env
```

### .env konfiguratsiya
```env
# Django
SECRET_KEY=your-very-long-and-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# PostgreSQL
USE_POSTGRES=True
DB_NAME=crmtizim_db
DB_USER=crmtizim_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Telegram (ixtiyoriy)
TELEGRAM_BOT_TOKEN=your_bot_token

# SMS (ixtiyoriy)
SMS_API_URL=https://notify.eskiz.uz/api
SMS_EMAIL=your_email
SMS_PASSWORD=your_password
```

---

## 5️⃣ Django Sozlash

### Migratsiyalar
```bash
python manage.py migrate
```

### Static fayllar
```bash
python manage.py collectstatic --noinput
```

### Superuser
```bash
python manage.py createsuperuser
```

### Media va logs papkalarni sozlash
```bash
sudo mkdir -p media logs
sudo chown -R www-data:www-data media logs
sudo chmod -R 755 media logs
```

---

## 6️⃣ Gunicorn Sozlash

### Log papkasini yaratish
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
```

### Service faylini ko'chirish
```bash
sudo cp systemd/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Statusni tekshirish
```bash
sudo systemctl status gunicorn
```

---

## 7️⃣ Nginx Sozlash

### Konfiguratsiyani ko'chirish
```bash
sudo cp nginx.conf /etc/nginx/sites-available/crmtizim
sudo ln -s /etc/nginx/sites-available/crmtizim /etc/nginx/sites-enabled/
```

### Domain nomini o'zgartirish
```bash
sudo nano /etc/nginx/sites-available/crmtizim
# server_name ni o'z domeningizga o'zgartiring
```

### Nginx ni test qilish va restart
```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 8️⃣ Celery Sozlash (Ixtiyoriy)

### Redis ni ishga tushirish
```bash
sudo systemctl start redis
sudo systemctl enable redis
```

### Celery Worker
```bash
sudo cp systemd/celery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start celery
sudo systemctl enable celery
```

### Celery Beat (Scheduled tasks)
```bash
sudo cp systemd/celery-beat.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start celery-beat
sudo systemctl enable celery-beat
```

---

## 9️⃣ SSL Certificate (HTTPS)

### Certbot o'rnatish
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### SSL yaratish
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Auto-renewal test
```bash
sudo certbot renew --dry-run
```

---

## 🔟 Firewall Sozlash

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

---

## 🔄 Auto Deployment

### Deploy skriptni ishlatish
```bash
chmod +x deploy.sh
```

### Yangilanishlarni olish
```bash
./deploy.sh
```

### Har safar GitHub ga push qilganda:
```bash
# Local kompyuterda
git add .
git commit -m "Your changes"
git push

# Serverda
cd /var/www/Crmtizim
./deploy.sh
```

---

## 📊 Monitoring va Logs

### Gunicorn logs
```bash
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log
```

### Nginx logs
```bash
sudo tail -f /var/nginx/error.log
sudo tail -f /var/nginx/access.log
```

### Django logs
```bash
tail -f logs/django.log
tail -f logs/errors.log
```

### Service status
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status celery
sudo systemctl status redis
```

---

## 🔧 Troubleshooting

### Gunicorn ishlamasa
```bash
# Loglarni tekshirish
sudo journalctl -u gunicorn -n 50 --no-pager

# Restart
sudo systemctl restart gunicorn

# Config test
/var/www/Crmtizim/venv/bin/gunicorn --check-config config.wsgi:application
```

### Nginx ishlamasa
```bash
# Config test
sudo nginx -t

# Error log
sudo tail -f /var/log/nginx/error.log

# Restart
sudo systemctl restart nginx
```

### PostgreSQL ulanmasa
```bash
# Status
sudo systemctl status postgresql

# Restart
sudo systemctl restart postgresql

# Connection test
psql -h localhost -U crmtizim_user -d crmtizim_db
```

### Static fayllar ko'rinmasa
```bash
python manage.py collectstatic --clear --noinput
sudo chown -R www-data:www-data staticfiles
sudo systemctl restart gunicorn nginx
```

### Permission errors
```bash
sudo chown -R www-data:www-data /var/www/Crmtizim
sudo chmod -R 755 /var/www/Crmtizim
sudo chmod -R 775 media logs
```

---

## 🎯 Post-Deployment Checklist

- [ ] PostgreSQL baza yaratildi va ulanish ishlayapti
- [ ] Virtual environment yaratildi va faollashtirildi
- [ ] Dependencies o'rnatildi
- [ ] .env fayl to'ldirildi
- [ ] Migratsiyalar bajarildi
- [ ] Static fayllar yig'ildi
- [ ] Superuser yaratildi
- [ ] Gunicorn ishga tushirildi
- [ ] Nginx ishga tushirildi
- [ ] Domain DNS sozlandi
- [ ] SSL certificate o'rnatildi
- [ ] Firewall sozlandi
- [ ] Celery ishga tushirildi (agar kerak bo'lsa)
- [ ] Backup strategiyasi o'rnatildi

---

## 🔐 Xavfsizlik

### SECRET_KEY yaratish
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### PostgreSQL password yaratish
```bash
openssl rand -base64 32
```

### .env faylni himoyalash
```bash
sudo chmod 600 .env
```

---

## 💾 Backup

### Database backup
```bash
# Backup yaratish
pg_dump -U crmtizim_user crmtizim_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore qilish
psql -U crmtizim_user crmtizim_db < backup_20260207_120000.sql
```

### Media fayllar backup
```bash
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Avtomatik backup (crontab)
```bash
crontab -e

# Har kuni soat 02:00 da backup
0 2 * * * pg_dump -U crmtizim_user crmtizim_db > /backups/db_$(date +\%Y\%m\%d).sql
```

---

## 📞 Yordam

- **GitHub Issues:** https://github.com/YOUR_USERNAME/Crmtizim/issues
- **Documentation:** Bu fayl
- **Email:** support@yourdomain.com

---

**© 2026 SMART EDU CRM**
