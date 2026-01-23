import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import User

print("=== O'QITUVCHILAR ===\n")
teachers = User.objects.filter(role='teacher')
for t in teachers:
    print(f"ID: {t.id}")
    print(f"  Ism: '{t.first_name}'")
    print(f"  Familiya: '{t.last_name}'")
    print(f"  Telefon: {t.phone}")
    print(f"  Full name: {t.full_name}")
    print()

if not teachers.exists():
    print("❌ O'qituvchilar topilmadi!")
