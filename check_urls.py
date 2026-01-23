"""
Check all URLs in settings page and sidebar
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

import django
django.setup()

from django.urls import reverse, NoReverseMatch

# Settings page URLs
settings_urls = [
    # Finance
    ('finance:category_list', 'Kategoriyalar'),
    ('finance:account_list', 'Kassalar'),
    ('finance:payroll_list', 'Oylik sozlamalari'),
    ('finance:report', 'Hisobotlar'),
    ('finance:category_create', 'Kategoriya qo\'shish'),
    ('finance:account_create', 'Kassa qo\'shish'),
    ('finance:add_income', 'Kirim qo\'shish'),
    ('finance:add_expense', 'Chiqim qo\'shish'),

    # Users
    ('users:user_list', 'Barcha foydalanuvchilar'),
    ('users:teacher_list', 'O\'qituvchilar'),
    ('users:student_list', 'O\'quvchilar'),
    ('users:staff_list', 'Xodimlar'),
    ('users:student_create', 'O\'quvchi qo\'shish'),
    ('users:teacher_create', 'O\'qituvchi qo\'shish'),

    # Education
    ('course_list', 'Kurslar'),
    ('group_list', 'Guruhlar'),
    ('room_list', 'Xonalar'),
    ('material_list', 'Materiallar'),
    ('course_create', 'Kurs qo\'shish'),
    ('group_create', 'Guruh qo\'shish'),
    ('room_create', 'Xona qo\'shish'),
    ('material_upload', 'Material yuklash'),

    # CRM
    ('crm:pipeline', 'Voronka'),
    ('crm:stage_list', 'Bosqichlar'),
    ('crm:source_list', 'Manbalar'),
    ('crm:lead_create', 'Yangi Lid'),

    # Operations
    ('operations:lesson_list', 'Darslar'),
    ('operations:schedule', 'Jadval'),
    ('operations:teacher_ratings', 'O\'qituvchi reytinglari'),
    ('operations:shop', 'Do\'kon'),

    # Core
    ('core:history_list', 'Tizim tarixi'),
    ('automation:template_list', 'Avtomatizatsiya'),
]

# Sidebar URLs
sidebar_urls = [
    ('dashboard', 'Dashboard'),
    ('users:user_list', 'Foydalanuvchilar'),
    ('automation:template_list', 'Avtomatizatsiya'),
    ('crm:pipeline', 'Voronka'),
    ('crm:stage_list', 'Bosqichlar'),
    ('crm:source_list', 'Manbalar'),
    ('group_list', 'Guruhlar'),
    ('course_list', 'Kurslar'),
    ('room_list', 'Xonalar'),
    ('material_list', 'Materiallar'),
    ('operations:lesson_list', 'Darslar'),
    ('operations:schedule', 'Jadval'),
    ('operations:teacher_ratings', 'O\'qituvchi reytinglari'),
    ('operations:student_ratings', 'O\'quvchi reytinglari'),
    ('operations:shop', 'Do\'kon'),
    ('finance:account_list', 'Kassalar'),
    ('finance:category_list', 'Kategoriyalar'),
    ('finance:transaction_list', 'Kirim-Chiqim'),
    ('finance:report', 'Hisobotlar'),
    ('finance:payroll_list', 'Oyliklar'),
    ('finance:staff_attendance_list', 'HR Davomat'),
    ('finance:supply_list', 'Sklad'),
    ('finance:pending_receipts', 'Chek Tekshirish'),
    ('core:settings', 'Sozlamalar'),
    ('core:history_list', 'Tarix'),
]

def check_urls(urls, title):
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print("=" * 60)

    ok_count = 0
    error_count = 0
    errors = []

    for url_name, description in urls:
        try:
            url = reverse(url_name)
            print(f"✓ {description:<30} → {url}")
            ok_count += 1
        except NoReverseMatch as e:
            print(f"✗ {description:<30} → XATO: {url_name}")
            error_count += 1
            errors.append((url_name, description))

    print("-" * 60)
    print(f"Natija: {ok_count} OK, {error_count} XATO")

    return errors

# Run checks
settings_errors = check_urls(settings_urls, "SETTINGS PAGE URLs")
sidebar_errors = check_urls(sidebar_urls, "SIDEBAR URLs")

print("\n" + "=" * 60)
print("UMUMIY NATIJA")
print("=" * 60)

if not settings_errors and not sidebar_errors:
    print("✅ BARCHA URL LAR ISHLAYAPTI!")
else:
    print("❌ XATOLAR TOPILDI:")
    for url_name, desc in settings_errors + sidebar_errors:
        print(f"   - {desc}: {url_name}")

