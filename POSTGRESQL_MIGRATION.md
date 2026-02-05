# 🚀 SQLite → PostgreSQL Migratsiya Qo'llanmasi

Bu qo'llanma sizga mavjud SQLite bazasidagi ma'lumotlarni PostgreSQL ga ko'chirishda yordam beradi.

## 📋 Talab qilinadigan narsalar

1. **PostgreSQL** o'rnatilgan bo'lishi kerak (v12+)
2. **Python 3.10+**
3. Virtual environment faollashtirilgan

---

## 🔧 1-QADAM: PostgreSQL o'rnatish (Agar o'rnatilmagan bo'lsa)

### Windows uchun:
1. [PostgreSQL rasmiy sayti](https://www.postgresql.org/download/windows/)dan yuklab oling
2. O'rnatish jarayonida **password** eslab qoling
3. O'rnatishdan so'ng, **pgAdmin** yoki **psql** orqali kiring

### Ubuntu/Debian uchun:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 🗄️ 2-QADAM: PostgreSQL baza yaratish

### 2.1 Terminal/CMD orqali psql ga kirish:

**Windows (PowerShell):**
```powershell
psql -U postgres
```

**Linux:**
```bash
sudo -u postgres psql
```

### 2.2 Quyidagi SQL buyruqlarini bajaring:

```sql
-- Foydalanuvchi yaratish
CREATE USER crmtizim_user WITH PASSWORD 'your_secure_password_here';

-- Baza yaratish
CREATE DATABASE crmtizim_db OWNER crmtizim_user;

-- Sozlamalar
ALTER ROLE crmtizim_user SET client_encoding TO 'utf8';
ALTER ROLE crmtizim_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crmtizim_user SET timezone TO 'Asia/Tashkent';

-- Huquqlar
GRANT ALL PRIVILEGES ON DATABASE crmtizim_db TO crmtizim_user;

-- PostgreSQL 15+ uchun qo'shimcha
\c crmtizim_db
GRANT ALL ON SCHEMA public TO crmtizim_user;

-- Chiqish
\q
```

---

## 📦 3-QADAM: SQLite dan ma'lumotlarni eksport qilish

**Virtual environment faol ekanligini tekshiring!**

```powershell
cd C:\Users\shona\PycharmProjects\Crmtizim

# Barcha ma'lumotlarni JSON formatda eksport qilish
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --indent 2 --output sqlite_backup.json
```

Bu buyruq `sqlite_backup.json` faylini yaratadi (hajmi katta bo'lishi mumkin).

---

## ⚙️ 4-QADAM: psycopg2 o'rnatish

```powershell
pip install psycopg2-binary
```

Agar xatolik chiqsa:
```powershell
pip install psycopg2
```

---

## 🔐 5-QADAM: .env faylini sozlash

Loyiha papkasida `.env` fayl yarating (`.env.example` dan nusxa oling):

```powershell
copy .env.example .env
```

`.env` faylini tahrirlang:

```env
# PostgreSQL faollashtirish
USE_POSTGRES=True

# PostgreSQL sozlamalari
DB_NAME=crmtizim_db
DB_USER=crmtizim_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
```

---

## 🏗️ 6-QADAM: PostgreSQL da jadvallarni yaratish

```powershell
# Migratsiyalarni qo'llash
python manage.py migrate
```

---

## 📤 7-QADAM: Ma'lumotlarni PostgreSQL ga yuklash

```powershell
# Ma'lumotlarni import qilish
python manage.py loaddata sqlite_backup.json
```

### Agar xatolik chiqsa:

**"ContentType already exists" xatosi:**
```powershell
python manage.py loaddata sqlite_backup.json --ignorenonexistent
```

**"Encoding" xatosi:**
```powershell
# Windows uchun
$env:PYTHONIOENCODING = "utf-8"
python manage.py loaddata sqlite_backup.json
```

---

## ✅ 8-QADAM: Tekshirish

```powershell
# Serverni ishga tushirish
python manage.py runserver

# Yoki shell orqali tekshirish
python manage.py shell
```

```python
# Django shell ichida
from apps.users.models import User
print(f"Foydalanuvchilar soni: {User.objects.count()}")

from apps.education.models import Course
print(f"Kurslar soni: {Course.objects.count()}")
```

---

## 🔄 Avtomatik skript (Ixtiyoriy)

Biz `migrate_to_postgres.py` skripti yaratdik. Uni ishlatish uchun:

```powershell
python migrate_to_postgres.py
```

Bu skript sizga qadamba-qadam migratsiya qilishda yordam beradi.

---

## ⚠️ Muhim eslatmalar

1. **Backup** - Har doim SQLite faylning nusxasini saqlang
2. **Password** - Kuchli parol ishlating
3. **Test** - Avval test muhitida sinab ko'ring
4. **Media fayllar** - `media/` papkasidagi fayllar alohida ko'chirilishi kerak (ular bazada saqlanmaydi)

---

## 🔙 Orqaga qaytish (SQLite ga)

Agar PostgreSQL bilan muammo chiqsa, `.env` faylida:

```env
USE_POSTGRES=False
```

Va serveringizni qayta ishga tushiring.

---

## 📞 Yordam

Muammo yuzaga kelsa, quyidagi fayllarni tekshiring:
- `logs/django.log`
- `logs/errors.log`

Yoki `python manage.py check` buyrug'ini bajaring.
