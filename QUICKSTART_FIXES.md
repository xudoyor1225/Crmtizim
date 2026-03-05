# O'zgarishlarni Qo'llash Bo'yicha Qo'llanma

## 🚀 Tezkor Boshlash

Ushbu o'zgarishlarni loyihaga qo'llash uchun quyidagi qadamlarni bajaring:

---

### 1-Qadam: Migratsiyalarni Qo'llash

```bash
# Virtual environmentni faollashtirish
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Yoki CMD:
venv\Scripts\activate

# Migratsiyalarni qo'llash
python manage.py migrate
```

Kutilgan natija:
```
Operations to perform:
  Apply all migrations: finance
Running migrations:
  Applying finance.0010_add_student_to_supply_transaction... OK
```

---

### 2-Qadam: Statik Fayllarni Yig'ish (Production uchun)

```bash
python manage.py collectstatic --noinput
```

---

### 3-Qadam: Serverni Qayta Ishga Tushirish

**Development server:**
```bash
# Serverni to'xtatish (Ctrl+C)
# Keyin qayta ishga tushirish
python manage.py runserver
```

**Production (Gunicorn):**
```bash
# systemd yordamida
sudo systemctl restart gunicorn

# Yoki to'g'ridan-to'g'ri
sudo systemctl restart your_project.service
```

**Celery worker va beat:**
```bash
sudo systemctl restart celery
sudo systemctl restart celery-beat
```

---

## ✅ Test Qilish

### 1. Administrator Dashboard Test

1. Admin sifatida login qiling
2. Dashboard ochilishini tekshiring
3. "To'lov Qabul Qilish" tugmasini bosing
4. Modal oynada 3 ta to'lov usuli borligini tekshiring:
   - 💵 Naqd pul
   - 💳 Plastik karta
   - 🏦 Terminal

### 2. Kassa Topshirish Test

1. Admin dashboard'da bir nechta tranzaksiya yarating
2. "Kassa Topshirish" sahifasiga o'ting
3. Topshirish yaratib, uni tasdiqlang
4. Detail sahifasida 3 ta ustun borligini tekshiring:
   - Naqd pul
   - Plastik karta
   - Terminal

### 3. Omborxona Test (Admin Role)

1. Admin role'da login qiling
2. "Omborxona" sahifasiga o'ting
3. Faqat **minus** (🔴) tugmasi borligini tekshiring
4. **Plus** (🟢) tugmasi yo'qligini tekshiring
5. Material yechishda "O'quvchi" selecti borligini tekshiring

### 4. Tranzaksiyani Bekor Qilish Test

1. Admin dashboard'da pending statusdagi tranzaksiya yarating
2. Tranzaksiya pastida "Bekor qilish" tugmasi borligini tekshiring
3. Tugmani bosib, operatsiyani tasdiqlang
4. Tranzaksiya bekor bo'lganligini va balance yangilanganligini tekshiring

### 5. Xavfsizlik Test

1. Pending tranzaksiya yarating
2. Kassa topshirish yarating va tasdiqlang
3. Topshirilgan tranzaksiyani bekor qilib bo'lmasligini tekshiring
4. Error xabari chiqishi kerak: "Tranzaksiya kassa topshirishda va tasdiqlangan. O'zgartirib bo'lmaydi!"

---

## 🔍 Muammolarni Bartaraf Qilish

### Agar migratsiya ishlamasa:

```bash
# Migratsiyalarni tekshirish
python manage.py showmigrations finance

# Fake migratsiyani qo'llash
python manage.py migrate finance zero
python manage.py migrate finance
```

### Agar static fayllar ko'rinmasa:

```bash
# Static fayllarni tozalash
python manage.py collectstatic --clear
python manage.py collectstatic --noinput
```

### Agar xatolik yuz bersa:

Loglarni tekshiring:
```bash
# Django logs
tail -f logs/error.log

# Gunicorn logs
journalctl -u gunicorn -f

# Celery logs
journalctl -u celery -f
```

---

## 📊 Ma'lumotlar Bazasi O'zgarishlari

### Yangi Maydonlar:

**SupplyTransaction model:**
- `student` (ForeignKey, nullable) - O'quvchi uchun material berish

**Transaction model:**
- `payment_method` choices o'zgardi:
  - ❌ 'transfer' (Bank o'tkazmasi) - o'chirildi
  - ❌ 'online' (Online to'lov) - o'chirildi
  - ✅ 'terminal' (Terminal) - qo'shildi

**CashSubmission model:**
- ❌ `amount_other` - o'chirildi

---

## 🎯 Rollar va Ruxsatlar

### Super Admin / Owner:
- ✅ Material qo'shish (+)
- ✅ Material yechish (-)
- ✅ Material tahrirlash (✏️)
- ✅ Material o'chirish (🗑️)
- ✅ O'quvchi tanlash

### Admin:
- ❌ Material qo'shish (+)
- ✅ Material yechish (-)
- ❌ Material tahrirlash (✏️)
- ❌ Material o'chirish (🗑️)
- ✅ O'quvchi tanlash

---

## 📝 Eslatmalar

1. **Importance:** Barcha o'zgarishlar production environment'da test qilinsin!
2. **Backup:** Ma'lumotlar bazasini backup qilish unutmang:
   ```bash
   python manage.py dumpdata > backup_$(date +%Y%m%d).json
   ```
3. **Rollback:** Agar muammo yuz bersa, git orqali qaytish:
   ```bash
   git stash
   # Yoki
   git reset --hard HEAD~1
   ```

---

## 🆘 Yordam

Muammolar yuzaga kelsa:
1. Loglarni tekshiring
2. FIXES_SUMMARY.md faylini o'qing
3. Development team bilan bog'laning

---

**Oxirgi yangilanish:** 2026-03-05  
**Versiya:** 1.0
