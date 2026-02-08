# Form va Modal Dizayni - Dark Mode Asosiy Tema ✅

## ❗ MUHIM O'ZGARISH

**Dark Mode endi asosiy tema!** Barcha inputlar va modallar dark blue fonda.

## Nima tuzatildi?

### 1. **Dark Mode - Asosiy Tema** 🌙
- Barcha input maydonlari **dark blue fon (navy-800)** bilan
- Border rangi: **navy-600** (to'q ko'k)
- Text rangi: **oq (#ffffff)**
- Placeholder: **kulrang ko'k**

### 2. **Modal Oynalari** 🔲
- Modal fon: **dark blue (navy-800)**
- Modal ichidagi barcha inputlar dark fonda
- Modal header va body dark blue

### 3. **Focus Effektlari** ✨
- Input maydonlariga focus qilinganda **ko'k border (#3b82f6)**
- Focus ring effekti: **ko'k soya** (3px rgba)
- Hover: **navy-500** border

### 4. **Tugma Dizaynlari** 🔘
- Submit tugmalari: Ko'k gradient (saqlanib qoldi)
- Cancel tugmalari: Kulrang
- Success tugmalari: Yashil gradient  
- Danger tugmalari: Qizil gradient

### 5. **Select va Textarea** 📝
- Barcha select dropdown dark fon
- Textarea maydonlari dark
- Checkbox va radio buttonlar dark

## Ranglar

### Dark Mode (Asosiy):
- **Fon**: `#0f1f35` (navy-800)
- **Border**: `#1c3255` (navy-600)
- **Text**: `#ffffff` (oq)
- **Placeholder**: `#64748b` (text-dim)
- **Focus border**: `#3b82f6` (accent-blue)
- **Focus shadow**: `rgba(59, 130, 246, 0.3)`

### Light Mode (Minimal):
- Faqat kerak bo'lganda ishlatiladi
- Default dark mode

## Serverda qo'llash

### 1. GitHub'dan yangilanishlarni olish:
```bash
cd /var/www/Crmtizim
git pull origin main
```

### 2. Static fayllarni to'plash:
```bash
source venv/bin/activate
python manage.py collectstatic --noinput
```

### 3. Gunicorn va Nginx'ni qayta ishga tushirish:
```bash
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

### 4. Tekshirish:
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
```

## Local'da test qilish

```bash
python manage.py runserver
```

Brauzerda: `http://127.0.0.1:8000`

## Tuzatilgan sahifalar

✅ Barcha form sahifalari (add, edit)
✅ Modal oynalari (qo'shish, tahrirlash, o'chirish)
✅ Student form
✅ Staff form  
✅ Lesson form
✅ Group form
✅ Material form
✅ va boshqalar...

## CSS Fayl

Yangilangan fayl: `static/css/style.css`

O'zgartirilgan qatorlar: **~500 qator** dark mode uchun

## Brauzer Qo'llab-quvvatlash

✅ Chrome/Edge
✅ Firefox
✅ Safari
✅ Mobile browsers

## Keyingi qadamlar

Agar yana ranglar yoki dizayn bo'yicha o'zgarishlar kerak bo'lsa:
1. `static/css/style.css` faylini tahrirlang
2. `python manage.py collectstatic --noinput` bajaring
3. Git'ga yuklang va serverga deploy qiling

---

**Eslatma**: Brauzer cache'ini tozalash kerak:
- `Ctrl+Shift+R` (Windows/Linux)
- `Cmd+Shift+R` (Mac)

## Screenshot

Endi formalar quyidagicha ko'rinadi:
- 🌙 Dark blue fon
- 📝 Oq text
- 🔵 Ko'k focus border
- ✨ Professional ko'rinish
