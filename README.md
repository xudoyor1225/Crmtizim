# 🎓 SMART EDU CRM - O'quv Markazlari uchun CRM & LMS Tizimi

## 📖 Loyiha Haqida

**SMART EDU CRM** - O'zbek o'quv markazlari uchun maxsus ishlab chiqilgan zamonaviy SaaS (Software as a Service) platformasi.

### ✨ Asosiy Imkoniyatlar:

#### 🎯 CRM (Mijozlar Boshqaruvi)
- 📞 Lid boshqaruvi (Lead Management)
- 🔄 Sotuv voronkasi (Sales Funnel)
- 📊 Kanban board
- 📱 SMS va Telegram integratsiyasi

#### 📚 LMS (Ta'lim Tizimi)
- 👨‍🎓 O'quvchilar bazasi
- 👨‍🏫 O'qituvchilar va guruhlar
- 📅 Dars jadvali
- ✅ Davomat tizimi
- 📝 Baholash va hisobotlar
- 📖 O'quv materiallari (Video, PDF, Audio)
- 📋 Syllabus (O'quv rejasi)

#### 💰 Moliya
- 💵 To'lovlar va chiqimlar
- 🏦 Kassa boshqaruvi
- 📊 Moliyaviy hisobotlar
- 💳 Plastik karta integratsiyasi
- 🧾 Chek yuklash va tasdiqlash

#### 👥 HR va Xodimlar
- 📋 Xodimlar bazasi
- ⏰ NFC turniket integratsiyasi
- 💼 Oylik hisob-kitob
- 📈 KPI (Key Performance Indicator)
- 📊 Davomat va kechikishlar

#### 🎮 Gamification
- ⭐ XP (Experience Points) tizimi
- 🏆 Badge (Nishonlar)
- 🔥 Streak (Ketma-ketlik)
- 🎯 Level tizimi

#### 🤖 Avtomatlashtirish
- 📨 Avtomatik SMS xabarnomalar
- 💬 Telegram bot
- ⏰ Dars eslatmalari
- 📊 Kunlik hisobotlar

---

## 🚀 O'rnatish va Ishga Tushirish

### 1️⃣ Talablar
- Python 3.10+
- PostgreSQL 13+ (yoki SQLite test uchun)
- Redis 6+ (Celery uchun)
- Git

### 2️⃣ Loyihani Yuklab Olish
```bash
git clone https://github.com/yourcompany/smartedu-crm.git
cd smartedu-crm
```

### 3️⃣ Virtual Environment Yaratish
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Kutubxonalarni O'rnatish
```bash
pip install -r requirements/base.txt
```

### 5️⃣ Environment O'rnatish
```bash
# .env.example dan .env yaratish
copy .env.example .env  # Windows
# yoki
cp .env.example .env    # Linux/Mac

# .env faylini tahrirlang va o'z sozlamalaringizni kiriting
```

### 6️⃣ Ma'lumotlar Bazasini Sozlash
```bash
# Migratsiyalarni yaratish
python manage.py makemigrations

# Migratsiyalarni bajarish
python manage.py migrate

# Super Admin yaratish
python manage.py createsuperuser
# Phone: 998900000000
# Password: admin123
```

### 7️⃣ Test Ma'lumotlarini Yuklash (Ixtiyoriy)
```bash
python setup_initial_data.py
```

### 8️⃣ **MUHIM: Darslarni Yaratish**
Guruhlar yaratilgandan keyin, ularning jadvaliga asoslanib darslar yaratish kerak:

```bash
# 4 haftalik darslar yaratish (default)
python generate_lessons.py

# Yoki boshqa vaqt uchun (masalan 8 hafta)
python generate_lessons.py 8
```

Bu script:
- ✅ Barcha faol guruhlarni oladi
- ✅ Ularning `schedule_days` maydoniga qarab darslar yaratadi
- ✅ Avtomatik o'qituvchi, xona va vaqtni belgilaydi
- ✅ Mavjud darslarni qayta yaratmaydi

### 9️⃣ Serverni Ishga Tushirish
```bash
python manage.py runserver
```

Brauzerda ochish: http://localhost:8000

---

## 📂 Loyiha Strukturasi

```
Crmtizim/
├── apps/                       # Barcha Django aplikatsiyalar
│   ├── core/                   # Asosiy funksiyalar
│   │   ├── models.py          # BaseModel, TenantAwareModel, AuditLog
│   │   ├── middleware.py      # TenantMiddleware (SaaS)
│   │   ├── permissions.py     # Role-based access control
│   │   └── validators.py      # File validation
│   ├── users/                  # Foydalanuvchilar
│   ├── organizations/          # Tashkilotlar va filiallar
│   ├── education/              # LMS (Guruhlar, Darslar)
│   ├── crm/                    # Lid va sotuv voronkasi
│   ├── finance/                # Moliya va kassa
│   ├── operations/             # Darslar, Davomat, Gamification
│   └── automation/             # SMS, Telegram bot
├── config/                     # Django sozlamalari
│   ├── settings/
│   │   ├── base.py            # Asosiy sozlamalar
│   │   ├── local.py           # Development
│   │   └── production.py      # Production
│   ├── urls.py                # URL routelar
│   └── celery.py              # Celery (background tasks)
├── templates/                  # HTML shablonlar
├── static/                     # CSS, JS, rasmlar
├── media/                      # Yuklangan fayllar
├── requirements/               # Python kutubxonalari
│   ├── base.txt               # Asosiy
│   └── production.txt         # Production
├── manage.py                   # Django CLI
├── .env.example               # Environment variables shabloni
└── README.md                   # Bu fayl
```

---

## 🔐 Xavfsizlik

### Environment Variables
Muhim ma'lumotlarni `.env` faylida saqlang:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### CORS Sozlamalari
Production'da faqat o'z domenlaringizni ruxsat bering:
```python
CORS_ALLOWED_ORIGINS = [
    'https://app.smartedu.uz',
    'https://admin.smartedu.uz',
]
```

### File Upload Xavfsizligi
Barcha fayllar validatsiyadan o'tadi:
- Fayl turi tekshiriladi
- Maksimal hajm cheklangan (5MB cheklar uchun, 100MB materiallar uchun)

---

## 👥 Rollar va Ruxsatlar

| Rol | Ruxsatlar |
|-----|-----------|
| **Super Admin** | Platforma egalari, barcha tashkilotlarga kirish |
| **Owner (Direktor)** | Markaz egasi, to'liq ruxsat |
| **Admin** | Filial boshqaruvchisi, ma'muriy ruxsatlar |
| **Teacher** | O'qituvchi, guruhlar va darslar |
| **Staff** | Xodim, cheklangan ruxsatlar |
| **Student** | O'quvchi, o'z ma'lumotlarini ko'rish |
| **Parent** | Ota-ona, farzand ma'lumotlarini ko'rish |

---

## 🔄 Background Tasks (Celery)

### Redis ni Ishga Tushirish
```bash
redis-server
```

### Celery Worker
```bash
celery -A config worker -l info
```

### Celery Beat (Scheduled Tasks)
```bash
celery -A config beat -l info
```

---

## 📊 API Endpoints

### REST API
```
GET  /api/students/          - O'quvchilar ro'yxati
POST /api/students/          - Yangi o'quvchi
GET  /api/groups/            - Guruhlar
POST /api/transactions/      - To'lov yaratish
```

### Authentication
```python
# Session Authentication (Web)
# Basic Authentication (API)
```

---

## 🧪 Testlar

### Testlarni Ishga Tushirish
```bash
python manage.py test
```

### Test Qamrovi
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚢 Production'ga Chiqarish

### 1. Environment O'rnatish
```env
DEBUG=False
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=yourdomain.com
```

### 2. Static Fayllarni Yig'ish
```bash
python manage.py collectstatic --noinput
```

### 3. PostgreSQL Sozlash
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=smartedu_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Gunicorn bilan Ishga Tushirish
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 5. Docker (Ixtiyoriy)
```bash
docker-compose up -d
```

---

## 📝 Muammolar va Yechimlar

### Muammo: Requirements o'rnatilmadi
```bash
pip install -r requirements/base.txt
```

### Muammo: Migration xatolari
```bash
python reset_db.py
python manage.py makemigrations
python manage.py migrate
```

### Muammo: Static fayllar yuklanmayapti
```bash
python manage.py collectstatic --clear
```

---

## 🤝 Hissa Qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. Commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

---

## 📞 Aloqa

- **Email:** support@smartedu.uz
- **Telegram:** @smartedu_support
- **Website:** https://smartedu.uz

---

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

---

## 🙏 Minnatdorchilik

- Django Framework
- Django REST Framework
- Tailwind CSS
- HTMX
- Va boshqa open-source kutubxonalarga!

---

**© 2024-2026 SMART EDU CRM. Barcha huquqlar himoyalangan.**
