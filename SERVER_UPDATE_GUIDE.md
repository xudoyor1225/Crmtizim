# 🚀 Server Yangilash Bo'yicha Qo'llanma

## ✅ Yangilanishlarni Serverga Qo'llash

### 1. SSH orqali serverga ulanish
```bash
ssh ubuntu@13.39.83.160
```

### 2. Loyiha papkasiga o'tish
```bash
cd /var/www/Crmtizim
source venv/bin/activate
```

### 3. GitHub'dan yangilanishlarni olish

#### A) Agar lokal o'zgarishlar bo'lsa:
```bash
# Lokal o'zgarishlarni vaqtincha saqlash
git stash

# GitHub'dan tortib olish
git pull origin main

# Static fayllarni yangilash
python manage.py collectstatic --noinput

# Servislarni qayta ishga tushirish
sudo systemctl restart gunicorn
sudo systemctl reload nginx

# Stash'dan qaytarish (kerak bo'lsa)
git stash pop
```

#### B) Lokal o'zgarishlar yo'q bo'lsa:
```bash
# To'g'ridan-to'g'ri tortib olish
git pull origin main

# Static fayllarni yangilash
python manage.py collectstatic --noinput

# Servislarni qayta ishga tushirish
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

### 4. Status tekshirish
```bash
# Gunicorn statusini ko'rish
sudo systemctl status gunicorn

# Nginx statusini ko'rish
sudo systemctl status nginx

# Loglarni monitoring qilish
sudo journalctl -u gunicorn -f
```

## 🔧 Muammolarni Hal Qilish

### Git Pull Muammolari

#### Divergent branches:
```bash
git config pull.rebase false
git pull origin main
```

#### Lokal o'zgarishlar:
```bash
# Saqlash
git stash
git pull origin main

# Yoki bekor qilish
git reset --hard HEAD
git pull origin main
```

### CSS O'zgarishlari Ko'rinmasa

```bash
# 1. Static fayllarni majburiy yangilash
python manage.py collectstatic --noinput --clear

# 2. Cache tozalash
rm -rf staticfiles/*
python manage.py collectstatic --noinput

# 3. Ruxsatlarni to'g'rilash
sudo chown -R ubuntu:www-data /var/www/Crmtizim/staticfiles
sudo chmod -R 755 /var/www/Crmtizim/staticfiles

# 4. Nginx'ni qayta ishga tushirish
sudo systemctl restart nginx
```

### Brauzer Cache'ini Tozalash

Server yangilangandan keyin:
- **Chrome/Edge**: `Ctrl + Shift + R`
- **Firefox**: `Ctrl + F5`
- **Safari**: `Cmd + Option + R`

## 📊 Monitoring

### Loglarni ko'rish:
```bash
# Django logs
tail -f logs/django.log

# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Service statuslari:
```bash
# Barcha statuslarni ko'rish
sudo systemctl status gunicorn nginx postgresql redis

# Qayta ishga tushirish
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🔐 GitHub Token

Agar push qilish kerak bo'lsa:

1. GitHub → Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic)
3. `repo` scope'ni belgilash
4. Token'ni nusxalash

```bash
# Token bilan push
git config --global credential.helper store
git push origin main
# Username: xudoyor1225
# Password: your_token_here
```

## 🎯 Tezkor Yangilash Buyruqlari

```bash
# Bitta buyruq bilan hammasi
cd /var/www/Crmtizim && \
source venv/bin/activate && \
git pull origin main && \
python manage.py collectstatic --noinput && \
sudo systemctl restart gunicorn && \
sudo systemctl reload nginx && \
echo "✅ Yangilandi!"
```

## ⚠️ Ehtiyot Choralari

- ✅ Har doim `venv`ni faollashtiring
- ✅ `collectstatic` ni ishlatishni unutmang
- ✅ Gunicorn'ni restart, Nginx'ni reload qiling
- ✅ Brauzer cache'ini tozalang
- ⚠️ Production'da bevosita o'zgartirish qilmang
- ⚠️ Doimo avval dev'da test qiling

## 📞 Yordam

Muammo yuzaga kelsa:
1. Loglarni tekshiring
2. Status'larni ko'ring
3. Nginx konfiguratsiyasini test qiling: `sudo nginx -t`
4. Gunicorn socket'ni tekshiring: `ls -la /var/www/Crmtizim/gunicorn.sock`

---

**Oxirgi yangilanish:** 2026-02-09
**Versiya:** 1.0
