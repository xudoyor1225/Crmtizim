# ⚠️ КЕНГ УЧРАЙДИГАН ХАТОЛАР ВА ЕЧИМЛАРИ

## 1️⃣ "can't open file 'manage.py'" хатоси

### ❌ Хато:
```
C:\Users\shona\PycharmProjects\Crmtizim\.venv/Scripts\python.exe: can't open file 
'C:\\Users\\shona\\PycharmProjects\\Crmtizim\\templates\\manage.py': [Errno 2] No such file or directory
```

### ✅ Сабаб:
Сиз нотўғри директорияда турибсиз. `manage.py` файли проект корневой папкасида (`Crmtizim/`), лекин сиз `templates/` папкасида турибсиз.

### ✅ Ечим:
```bash
# Проект корневой папкасига ўтинг
cd C:\Users\shona\PycharmProjects\Crmtizim

# Энди серверни ишга туширинг
python manage.py runserver
```

### 📝 Қоида:
Django командаларини **ДОИМ** проект корневой папкасидан (қаерда `manage.py` бор) ишга тушинг!

---

## 2️⃣ "Port already in use" хатоси

### ❌ Хато:
```
Error: That port is already in use.
```

### ✅ Ечим:
```bash
# 1-usul: Boshqa portda ishga tushiring
python manage.py runserver 8080

# 2-usul: Eski jarayonni to'xtating
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Keyin qayta urinib ko'ring
python manage.py runserver
```

---

## 3️⃣ "No module named..." хатоси

### ❌ Хато:
```
ModuleNotFoundError: No module named 'django'
```

### ✅ Ечим:
```bash
# Virtual environment aktivlashtiring
.venv\Scripts\activate

# Dependencies o'rnating
pip install -r requirements/base.txt
```

---

## 4️⃣ Migration хатолари

### ❌ Хато:
```
django.db.utils.OperationalError: no such table: ...
```

### ✅ Ечим:
```bash
# Migratsiyalarni yarating
python manage.py makemigrations

# Migratsiyalarni qo'llang
python manage.py migrate
```

---

## 5️⃣ Static фай��лар юкланмайди

### ❌ Муаммо:
CSS, JS файллар браузерда юкланмайди

### ✅ Ечим:
```bash
# Static fayllarni to'plang
python manage.py collectstatic

# Yoki DEBUG=True rejimida ishga tushiring
# settings/base.py da:
DEBUG = True
```

---

## 6️⃣ "Permission denied" хатоси

### ❌ Хато:
```
PermissionError: [WinError 5] Access is denied
```

### ✅ Ечим:
```bash
# Administrator sifatida terminal oching
# Yoki:
# Fayllar ustiga Right-click → Properties → Unblock
```

---

## 7️⃣ "Invalid HTTP_HOST header" хатоси

### ❌ Хато:
```
Invalid HTTP_HOST header: '...'
```

### ✅ Ечим:
```python
# config/settings/base.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']  # Development uchun
```

---

## 8️⃣ Bazani tozalash kerak

### ✅ Ечим:
```bash
# 1-usul: Ma'lumotlarni to'liq o'chirish
python manage.py flush

# 2-usul: Database faylini o'chirish (SQLite)
del db.sqlite3
python manage.py migrate

# 3-usul: Yangi test ma'lumotlar yaratish
python manage.py populate_data
python manage.py generate_lessons --weeks 4
```

---

## 9️⃣ Template хатолари

### ❌ Хато:
```
TemplateDoesNotExist at /...
```

### ✅ Ечим:
```python
# settings.py da template papkalarni tekshiring:
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

---

## 🔟 Parol esdan chiqqan

### ✅ Ечим:
```bash
# Yangi superuser yarating
python manage.py createsuperuser

# Yoki mavjud userning parolini o'zgartiring
python manage.py changepassword username
```

---

## 📋 TEZKOR YORDAM KOMANDALAR

### Serverni ishga tushirish:
```bash
cd C:\Users\shona\PycharmProjects\Crmtizim
.venv\Scripts\activate
python manage.py runserver
```

### Test ma'lumotlarni yaratish:
```bash
python manage.py populate_data
python manage.py generate_lessons --weeks 4
```

### Migratsiyalar:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell ochish (debug uchun):
```bash
python manage.py shell
```

### Barcha xatolarni tekshirish:
```bash
python manage.py check
python manage.py check --deploy
```

---

## 🆘 YORDAM KERAKMI?

### Xatoni to'liq nusxalang:
```
1. Xato matni
2. Qaysi komanda ishlatilgan
3. Qaysi papkada turganingiz
```

### Loglarni tekshiring:
```
logs/django.log
logs/errors.log
```

### DEBUG rejimini yoqing:
```python
# settings/base.py
DEBUG = True
```

---

## ✅ TO'G'RI ISHCHI OQIM

```bash
# 1. Papkani tekshiring
pwd  # Linux/Mac
cd   # Windows

# 2. To'g'ri papkaga o'ting
cd C:\Users\shona\PycharmProjects\Crmtizim

# 3. Virtual environment aktivlashtiring
.venv\Scripts\activate

# 4. Serverni ishga tushiring
python manage.py runserver

# 5. Brauzerni oching
# http://127.0.0.1:8000
```

---

**Eslatma**: Барча Django командалари учун проект корневой папкасида (`Crmtizim/`) туришингиз шарт! 📌
