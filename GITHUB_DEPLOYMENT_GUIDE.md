# 🚀 GitHub va Server Deployment - Final Steps

## ✅ HOZIRGI HOLAT

**Loyiha tayyor:**
- ✅ Barcha kodlar commit qilindi (3 ta commit)
- ✅ PostgreSQL ga migratsiya tugadi
- ✅ Deployment scripts yaratildi
- ✅ Documentation to'liq yozildi
- ✅ .gitignore yangilandi

**Branch:** master
**Commits ahead:** 3 ta (push qilinmagan)

---

## 📋 1-QADAM: GitHub Repository Yaratish

### 1.1 GitHub ga kiring
```
https://github.com/login
```

### 1.2 Yangi Repository yaratish
```
https://github.com/new
```

**Sozlamalar:**
- **Repository name:** `Crmtizim` (yoki `smartedu-crm`)
- **Description:** `🎓 O'quv Markazlari uchun CRM & LMS Tizimi - Django, PostgreSQL`
- **Visibility:** Public yoki Private (tanlang)
- **⚠️ MUHIM:** README, .gitignore, LICENSE **QO'SHMANG** (bizda mavjud)
- **Create repository** tugmasini bosing

---

## 📋 2-QADAM: Local Repository ni GitHub ga Ulash

### 2.1 PowerShell da (Crmtizim papkasida)

```powershell
cd C:\Users\shona\PycharmProjects\Crmtizim

# Remote qo'shish (YOUR_USERNAME o'rniga GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Crmtizim.git

# Branch nomini tekshirish
git branch

# Agar master bo'lsa, main ga o'zgartirish (tavsiya etiladi)
git branch -M main

# Push qilish
git push -u origin main
```

**Namuna (o'z username bilan):**
```powershell
git remote add origin https://github.com/xudoyor1225/Crmtizim.git
git branch -M main
git push -u origin main
```

---

## 📋 3-QADAM: Authentication

### 3.1 Username va Password so'raladi

**Username:** GitHub username (masalan: `xudoyor1225`)

**Password:** ❌ GitHub parolingiz EMAS! Personal Access Token kerak

### 3.2 Personal Access Token Yaratish

1. **GitHub Settings ga o'ting:**
   ```
   https://github.com/settings/tokens
   ```

2. **"Generate new token" → "Generate new token (classic)"**

3. **Sozlamalar:**
   - **Note:** `Crmtizim Local Development`
   - **Expiration:** `90 days` yoki `No expiration`
   - **Scopes:** ✅ Faqat `repo` (full control of private repositories)

4. **"Generate token" tugmasini bosing**

5. **Token ni nusxa oling:**
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   ⚠️ **MUHIM:** Bu tokenni xavfsiz saqlang! Qayta ko'ra olmaysiz.

6. **PowerShell da password o'rniga tokenni kiriting:**
   ```
   Username: xudoyor1225
   Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 📋 4-QADAM: Push Muvaffaqiyatli Bo'lsa

### 4.1 Terminal da ko'rinadi:
```
Enumerating objects: 500, done.
Counting objects: 100% (500/500), done.
Compressing objects: 100% (350/350), done.
Writing objects: 100% (500/500), 2.5 MiB | 500 KiB/s, done.
Total 500 (delta 200), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/Crmtizim.git
 * [new branch]      main -> main
```

### 4.2 GitHub da tekshiring:
```
https://github.com/YOUR_USERNAME/Crmtizim
```

**Ko'rinishi kerak:**
- ✅ Barcha fayllar
- ✅ README.md to'g'ri render bo'ladi
- ✅ 3 ta commit tarixi
- ✅ Papkalar strukturasi

---

## 📋 5-QADAM: Repository Sozlash

### 5.1 About bo'limini to'ldirish
Repository sahifasida yuqorida "⚙️ Settings" yonida "About" bo'ladi:

- **Description:** `🎓 O'quv Markazlari uchun CRM & LMS Tizimi`
- **Website:** (agar bor bo'lsa)
- **Topics:** `django`, `crm`, `lms`, `education`, `postgresql`, `saas`, `uzbekistan`, `python`

### 5.2 Branch sozlash (ixtiyoriy)
Settings → Branches → Default branch → `main`

---

## 📋 6-QADAM: Serverga Deploy Qilish

### 6.1 Server tayyorlash (Ubuntu 22.04)

```bash
# SSH orqali serverga kirish
ssh user@your-server-ip

# Dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip \
    postgresql postgresql-contrib nginx redis-server git \
    build-essential libpq-dev

# PostgreSQL
sudo -u postgres psql
CREATE DATABASE crmtizim_db;
CREATE USER crmtizim_user WITH PASSWORD 'your_secure_password';
ALTER ROLE crmtizim_user SET client_encoding TO 'utf8';
ALTER ROLE crmtizim_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE crmtizim_db TO crmtizim_user;
\c crmtizim_db
GRANT ALL ON SCHEMA public TO crmtizim_user;
\q
```

### 6.2 Clone va Setup

```bash
# Clone
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/Crmtizim.git
sudo chown -R $USER:$USER Crmtizim
cd Crmtizim

# Virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Dependencies
pip install --upgrade pip
pip install -r requirements/base.txt
pip install gunicorn

# .env fayl
cp .env.example .env
nano .env
```

### 6.3 .env Configuration (Production)

```env
# Django
SECRET_KEY=<generate-with-command-below>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# PostgreSQL
USE_POSTGRES=True
DB_NAME=crmtizim_db
DB_USER=crmtizim_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis (ixtiyoriy)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**SECRET_KEY yaratish:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6.4 Django Setup

```bash
# Migratsiya
python manage.py migrate

# Static files
python manage.py collectstatic --noinput

# Superuser
python manage.py createsuperuser

# Permissions
sudo mkdir -p /var/log/gunicorn logs
sudo chown -R www-data:www-data /var/log/gunicorn logs media
```

### 6.5 Services

```bash
# Gunicorn
sudo cp systemd/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

# Nginx
sudo cp nginx.conf /etc/nginx/sites-available/crmtizim

# nginx.conf da domain nomini o'zgartirish
sudo nano /etc/nginx/sites-available/crmtizim
# server_name yourdomain.com www.yourdomain.com; → o'z domeningiz

sudo ln -s /etc/nginx/sites-available/crmtizim /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Celery (ixtiyoriy)
sudo cp systemd/celery.service systemd/celery-beat.service /etc/systemd/system/
sudo systemctl start celery celery-beat
sudo systemctl enable celery celery-beat
```

### 6.6 Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 6.7 SSL Certificate (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📋 7-QADAM: Yangilanishlar (Git Push → Server Deploy)

### 7.1 Local da o'zgarish qilganingizda:

```powershell
cd C:\Users\shona\PycharmProjects\Crmtizim

git add .
git commit -m "Your changes description"
git push
```

### 7.2 Server da yangilanishni olish:

```bash
cd /var/www/Crmtizim
./deploy.sh
```

**deploy.sh avtomatik bajaradi:**
- ✅ Git pull origin main
- ✅ pip install -r requirements/base.txt
- ✅ python manage.py migrate
- ✅ python manage.py collectstatic --noinput
- ✅ sudo systemctl restart gunicorn nginx

---

## 🔧 Troubleshooting

### ❌ Git push xatosi: "Authentication failed"
**Yechim:** Personal Access Token ishlatganingizni tekshiring, parol emas!

### ❌ Git push xatosi: "remote: Permission denied"
**Yechim:** Repository owner ekanligingizni tekshiring yoki token scope `repo` borligini.

### ❌ "fatal: remote origin already exists"
**Yechim:**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/Crmtizim.git
```

### ❌ Server da "Permission denied"
**Yechim:**
```bash
sudo chown -R www-data:www-data /var/www/Crmtizim
sudo chmod -R 755 /var/www/Crmtizim
```

### ❌ Gunicorn ishlamasa
**Yechim:**
```bash
sudo journalctl -u gunicorn -n 50 --no-pager
sudo systemctl restart gunicorn
```

### ❌ Static files ko'rinmasa
**Yechim:**
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart gunicorn nginx
```

---

## 📚 Qo'shimcha Qo'llanmalar

| Fayl | Maqsad |
|------|--------|
| **README.md** | Loyiha haqida, o'rnatish |
| **QUICKSTART.md** | Tezkor boshlash (local) |
| **POSTGRESQL_MIGRATION.md** | SQLite → PostgreSQL |
| **DEPLOYMENT.md** | Server deployment (batafsil) |
| **DEPLOYMENT_READY.md** | Deployment (qisqacha) |

---

## ✅ Checklist

**GitHub:**
- [ ] Repository yaratildi
- [ ] Remote qo'shildi
- [ ] Push qilindi
- [ ] README.md to'g'ri ko'rinadi
- [ ] About to'ldirildi

**Server:**
- [ ] Server tayyorlandi
- [ ] PostgreSQL o'rnatildi va database yaratildi
- [ ] Clone qilindi
- [ ] .env sozlandi
- [ ] Migratsiya qilindi
- [ ] Gunicorn ishga tushirildi
- [ ] Nginx sozlandi
- [ ] Domain DNS sozlandi
- [ ] SSL certificate olindi
- [ ] deploy.sh ishga tushirildi

---

## 🎯 Keyingi Qadamlar

1. **GitHub ga push qilish** (yuqoridagi ko'rsatmalarga amal qiling)
2. **Server sozlash** (DEPLOYMENT.md ni kuzatib)
3. **Test qilish** (http://yourdomain.com)
4. **Monitoring sozlash** (logs, backups)

---

## 📞 Yordam Kerakmi?

- **DEPLOYMENT.md** - To'liq server qo'llanmasi (250+ qator)
- **GitHub Docs** - https://docs.github.com
- **Loglar** - Har doim loglarni tekshiring

---

**© 2026 SMART EDU CRM - Ready for Production! 🚀**

**P.S.** GitHub token yaratishda muammo bo'lsa, screenshot bilan savol bering!
