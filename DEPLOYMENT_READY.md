# 🎯 DEPLOYMENT READY - Server Deployment Configuration

## ✅ Tayyor Fayllar

### 🚀 Deployment Scripts
- **`deploy.sh`** - Avtomatik deployment skript
  - Git pull
  - Dependencies o'rnatish
  - Migratsiya
  - Static files
  - Services restart

### ⚙️ Server Configuration
- **`gunicorn_config.py`** - Gunicorn WSGI server sozlamalari
- **`nginx.conf`** - Nginx web server konfiguratsiyasi
- **`systemd/gunicorn.service`** - Gunicorn systemd service
- **`systemd/celery.service`** - Celery worker service
- **`systemd/celery-beat.service`** - Celery beat scheduler

### 📖 Documentation
- **`DEPLOYMENT.md`** - To'liq server deployment qo'llanmasi
  - Server tayyorlash
  - PostgreSQL sozlash
  - Nginx, Gunicorn setup
  - SSL certificate
  - Troubleshooting

### 🔧 Code Updates
- **`config/settings/production.py`** - Production sozlamalari
  - DEBUG=False
  - HTTPS sozlamalari
  - Security headers
  - Logging configuration
- **`.env.example`** - Environment variables example (fixed typos)

---

## 🚀 GitHub ga Yuklash

### 1. GitHub Repository Yaratish
```
https://github.com/new
Repository name: Crmtizim
Description: 🎓 O'quv Markazlari uchun CRM & LMS Tizimi
Public/Private: Tanlang
```

### 2. Local Repository ni GitHub ga Ulash
```powershell
cd C:\Users\shona\PycharmProjects\Crmtizim

# Remote qo'shish (YOUR_USERNAME o'rniga GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Crmtizim.git

# Branch nomini main qilish
git branch -M main

# Push qilish
git push -u origin main
```

### 3. Authentication
Agar token so'ralsa:
- Username: GitHub username
- Password: Personal Access Token
  - Token yaratish: https://github.com/settings/tokens
  - Scopes: `repo` (full control)

---

## 🖥️ Serverga Deploy Qilish

### Quick Start (Ubuntu 22.04)

```bash
# 1. Server ga SSH orqali kirish
ssh user@your-server-ip

# 2. Kerakli paketlarni o'rnatish
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip \
    postgresql postgresql-contrib nginx redis-server git

# 3. PostgreSQL sozlash
sudo -u postgres psql
CREATE DATABASE crmtizim_db;
CREATE USER crmtizim_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE crmtizim_db TO crmtizim_user;
\q

# 4. Loyihani clone qilish
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/Crmtizim.git
cd Crmtizim

# 5. Virtual environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
pip install gunicorn

# 6. .env sozlash
cp .env.example .env
nano .env  # O'zgartirishlar kiriting

# 7. Django sozlash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 8. Gunicorn service
sudo cp systemd/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 9. Nginx sozlash
sudo cp nginx.conf /etc/nginx/sites-available/crmtizim
sudo ln -s /etc/nginx/sites-available/crmtizim /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. Celery (ixtiyoriy)
sudo cp systemd/celery.service /etc/systemd/system/
sudo systemctl start celery
sudo systemctl enable celery
```

---

## 🔄 Yangilanishlarni Deploy Qilish

### Local da (development):
```powershell
# O'zgarishlar qilish
git add .
git commit -m "Your changes"
git push
```

### Server da:
```bash
cd /var/www/Crmtizim
./deploy.sh
```

**`deploy.sh` avtomatik bajaradi:**
- ✅ Git pull
- ✅ Dependencies update
- ✅ Database migration
- ✅ Static files collection
- ✅ Services restart

---

## 📊 Tekshirish

### Services Status
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status celery
```

### Logs Ko'rish
```bash
# Gunicorn
sudo tail -f /var/log/gunicorn/error.log

# Nginx
sudo tail -f /var/log/nginx/error.log

# Django
tail -f logs/django.log
```

### Browser da Test
```
http://your-server-ip        # HTTP
https://yourdomain.com       # HTTPS (SSL certificate dan keyin)
```

---

## 🔐 Xavfsizlik

### SECRET_KEY Yaratish
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Firewall
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 📁 .env File (Production)

```env
# Django
SECRET_KEY=<strong-secret-key-from-above-command>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# PostgreSQL
USE_POSTGRES=True
DB_NAME=crmtizim_db
DB_USER=crmtizim_user
DB_PASSWORD=<your-secure-password>
DB_HOST=localhost
DB_PORT=5432

# Redis (optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## 🐛 Troubleshooting

### Permission Errors
```bash
sudo chown -R www-data:www-data /var/www/Crmtizim
sudo chmod -R 755 /var/www/Crmtizim
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart gunicorn nginx
```

### Database Connection Error
```bash
# Test connection
psql -h localhost -U crmtizim_user -d crmtizim_db

# Check PostgreSQL status
sudo systemctl status postgresql
```

---

## 📞 Qo'shimcha Yordam

- **Documentation:** `DEPLOYMENT.md` faylini o'qing
- **GitHub Issues:** Repository issues bo'limida savol bering
- **Logs:** Har doim loglarni tekshiring

---

## ✅ Checklist

Serverga deploy qilishdan oldin:
- [ ] GitHub repository yaratildi
- [ ] Local code GitHub ga push qilindi
- [ ] Server tayyorlandi (Ubuntu 22.04+)
- [ ] PostgreSQL o'rnatildi va database yaratildi
- [ ] .env fayl to'ldirildi
- [ ] Domain DNS sozlandi (agar bor bo'lsa)
- [ ] SSL certificate olindi (HTTPS uchun)
- [ ] Backup strategiyasi o'rnatildi

---

**© 2026 SMART EDU CRM - Ready for Production! 🚀**
