# 🚀 TEZKOR BOSHLASH QOLLANMASI

## 1️⃣ O'RNATISH

```bash
# Virtual environment yaratish
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Dependencies o'rnatish
pip install -r requirements/base.txt

# Database yaratish
python manage.py migrate
```

## 2️⃣ TEST MA'LUMOTLARNI YARATISH

```bash
# Avtomatik test ma'lumotlarni yaratish
python manage.py populate_data

# Darslarni generatsiya qilish (4 haftalik)
python manage.py generate_lessons --weeks 4
```

Bu command quyidagilarni yaratadi:
- ✅ 1 ta Tashkilot
- ✅ 1 ta Filial
- ✅ 1 ta Admin + 3 ta O'qituvchi + 6 ta O'quvchi
- ✅ 3 ta Kurs (IELTS, English, Python)
- ✅ 4 ta Xona
- ✅ 3 ta Guruh (har birida 2 tadan o'quvchi)
- ✅ 3 ta Kassa
- ✅ 7 ta Kategoriya
- ✅ 3 ta To'lov
- ✅ 5 ta CRM Bosqich
- ✅ 5 ta CRM Manba
- ✅ 3 ta Lead

## 3️⃣ SERVERNI ISHGA TUSHIRISH

```bash
python manage.py runserver
```

Brauzerda oching: http://127.0.0.1:8000

## 4️⃣ LOGIN QILISH

```
👤 Admin:
   Telefon: +998901111111
   Parol:   admin123

👨‍🏫 O'qituvchi:
   Telefon: +99890jasu
   Parol:   teacher123

👨‍🎓 O'quvchi:
   Telefon: +998911001000
   Parol:   student123
```

## 5️⃣ ASOSIY SAHIFALAR

### Dashboard & Sozlamalar
- 🏠 Dashboard: http://127.0.0.1:8000/
- ⚙️ Sozlamalar: http://127.0.0.1:8000/core/settings/
- 📜 Tarix: http://127.0.0.1:8000/core/history/

### Ta'lim
- 📚 Kurslar: http://127.0.0.1:8000/courses/
- 👥 Guruhlar: http://127.0.0.1:8000/groups/
- 🚪 Xonalar: http://127.0.0.1:8000/rooms/
- 📹 Materiallar: http://127.0.0.1:8000/edu/materials/

### Darslar
- 📖 Darslar: http://127.0.0.1:8000/operations/lessons/
- 📅 Jadval: http://127.0.0.1:8000/operations/schedule/
- 🏆 Reytinglar: http://127.0.0.1:8000/operations/ratings/teachers/

### Moliya
- 💰 Kassalar: http://127.0.0.1:8000/finance/accounts/
- 📁 Kategoriyalar: http://127.0.0.1:8000/finance/categories/
- 💳 Tranzaksiyalar: http://127.0.0.1:8000/finance/transactions/
- 💵 Oyliklar: http://127.0.0.1:8000/finance/payroll/
- 📊 Hisobotlar: http://127.0.0.1:8000/finance/reports/

### CRM
- 🎯 Pipeline: http://127.0.0.1:8000/crm/pipeline/
- 👥 O'quvchilar: http://127.0.0.1:8000/crm/students/

## 6️⃣ FOYDALI COMMANDLAR

```bash
# Yangi superuser yaratish
python manage.py createsuperuser

# Admin panel: http://127.0.0.1:8000/admin/

# Ma'lumotlarni backup qilish
python manage.py dumpdata > backup.json

# Ma'lumotlarni restore qilish
python manage.py loaddata backup.json

# Database ni tozalash
python manage.py flush

# Test ma'lumotlarni qayta yaratish
python manage.py populate_data
python manage.py generate_lessons --weeks 4
```

## 7️⃣ MUAMMOLARNI HAL QILISH

### Server ishlamayapti?
```bash
# Port band bo'lsa
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Yoki boshqa portda ishga tushiring
python manage.py runserver 8080
```

### Migration xatolari?
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static fayllar yuklanmayapti?
```bash
python manage.py collectstatic
```

## 8️⃣ QOSHIMCHA HUJJATLAR

- 📄 [FINAL_REPORT.md](FINAL_REPORT.md) - To'liq hisobot
- 📄 [FIXES_REPORT.md](FIXES_REPORT.md) - Tuzatishlar hisoboti
- 📄 [project_context.md](project_context.md) - Loyiha konteksti

## 9️⃣ YANGI XUSUSIYAT QOSHISH

### Yangi Kategoriya qo'shish:
1. Sozlamalar → Moliya → Kategoriyalar → [+ Qo'shish]
2. Yoki: http://127.0.0.1:8000/finance/categories/add/

### Yangi Kurs qo'shish:
1. Sozlamalar → Ta'lim → Kurslar → [+ Qo'shish]
2. Yoki: http://127.0.0.1:8000/courses/add/

### Yangi Guruh qo'shish:
1. Guruhlar → [+ Yangi Guruh]
2. Dars kunlarini tanlang (checkbox)
3. Saqlang
4. `python manage.py generate_lessons --weeks 4` ni ishga tushiring

## 🔟 PRODUCTION GA CHIQARISH

```bash
# 1. Settings ni production ga o'zgartiring
# config/settings/production.py

# 2. Secret key yarating
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. PostgreSQL database sozlang
# 4. Static fayllarni to'plang
python manage.py collectstatic

# 5. Gunicorn yoki uWSGI orqali ishga tushiring
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

**Savol-javoblar uchun**: [GitHub Issues](https://github.com/your-repo/issues)  
**Muallif**: Smart Edu Team  
**Versiya**: 1.0.0  
**Sana**: 2026-01-23
