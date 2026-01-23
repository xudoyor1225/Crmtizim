import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.organizations.models import Organization, Branch
from apps.users.models import User, ParentStudent
from apps.education.models import Course, Room, Group, GroupStudent
from apps.crm.models import Stage, LeadSource, Lead
from apps.finance.models import Account, TransactionCategory, Transaction

# O'zbek ismlari
FIRST_NAMES_MALE = ["Alisher", "Jasur", "Sardor", "Bekzod", "Shoxrux", "Azizbek", "Nodir", "Oybek", "Temur", "Doniyor"]
FIRST_NAMES_FEMALE = ["Nilufar", "Gulnora", "Malika", "Aziza", "Madina", "Zarina", "Dilnoza", "Shahzoda", "Feruza", "Kamola"]
LAST_NAMES = ["Karimov", "Toshmatov", "Saidov", "Raximov", "Yusupov", "Xolmatov", "Qodirov", "Ergashev", "Normatov", "Mirzayev"]

# Kurslar
COURSES = [
    ("IELTS", 1500000, 3),
    ("Frontend", 2000000, 6),
    ("Backend Python", 2500000, 6),
    ("Mobile Development", 2200000, 5),
    ("Ingliz tili (Boshlang'ich)", 800000, 3),
    ("Rus tili", 600000, 2),
    ("Matematika", 500000, 3),
]

def generate_phone():
    return f"9989{random.randint(10000000, 99999999)}"

def setup():
    print("=" * 50)
    print("🚀 SMART EDU - Test ma'lumotlarini yaratish")
    print("=" * 50)
    
    # 1. TASHKILOT
    if not Organization.objects.exists():
        org = Organization.objects.create(
            name="Najot Ta'lim",
            subdomain="najot",
            config={"theme": "dark", "currency": "UZS"}
        )
        print(f"✅ Tashkilot yaratildi: {org.name}")
    else:
        org = Organization.objects.first()
        print(f"📌 Mavjud tashkilot: {org.name}")

    # 2. FILIALLAR
    branches = []
    branch_names = ["Chilonzor filiali", "Sergeli filiali", "Yunusobod filiali"]
    for name in branch_names:
        branch, created = Branch.objects.get_or_create(
            organization=org,
            name=name,
            defaults={
                "address": f"Toshkent, {name}",
                "phone": generate_phone()
            }
        )
        branches.append(branch)
        if created:
            print(f"✅ Filial yaratildi: {name}")
    
    main_branch = branches[0]

    # 3. SUPER ADMIN
    if not User.objects.filter(role='super_admin').exists():
        admin = User.objects.create_superuser(
            phone="998900000000",
            password="admin",
            first_name="Super",
            last_name="Admin",
            role="super_admin",
            organization=org,
            branch=main_branch
        )
        print(f"✅ Super Admin yaratildi: 998900000000 / admin")
    else:
        print(f"📌 Super Admin mavjud: 998900000000 / admin")

    # 4. O'QITUVCHILAR (5 ta)
    teachers = []
    for i in range(5):
        phone = generate_phone()
        teacher, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                "first_name": random.choice(FIRST_NAMES_MALE),
                "last_name": random.choice(LAST_NAMES),
                "role": "teacher",
                "organization": org,
                "branch": random.choice(branches),
                "nfc_card_id": f"NFC-{1000+i}",
                "profile_data": {"passport_series": f"AA{random.randint(1000000, 9999999)}"}
            }
        )
        if created:
            teacher.set_password("teacher123")
            teacher.save()
        teachers.append(teacher)
    print(f"✅ {len(teachers)} ta o'qituvchi yaratildi/mavjud")

    # 5. XONALAR
    rooms = []
    for i in range(1, 6):
        room, _ = Room.objects.get_or_create(
            branch=main_branch,
            name=f"Xona #{i}",
            defaults={"capacity": random.randint(15, 30)}
        )
        rooms.append(room)
    print(f"✅ {len(rooms)} ta xona yaratildi/mavjud")

    # 6. KURSLAR
    courses = []
    for name, price, duration in COURSES:
        course, _ = Course.objects.get_or_create(
            organization=org,
            name=name,
            defaults={
                "base_price": price,
                "duration_months": duration,
                "description": f"{name} kursi haqida ma'lumot"
            }
        )
        courses.append(course)
    print(f"✅ {len(courses)} ta kurs yaratildi/mavjud")

    # 7. GURUHLAR (10 ta)
    groups = []
    for i in range(10):
        course = random.choice(courses)
        teacher = random.choice(teachers)
        group, created = Group.objects.get_or_create(
            branch=random.choice(branches),
            name=f"{course.name[:4].upper()}-{100+i}",
            defaults={
                "course": course,
                "teacher": teacher,
                "status": random.choice(["forming", "active", "active", "active"]),
                "start_date": datetime.now().date() - timedelta(days=random.randint(0, 60)),
                "schedule_days": random.choice([[1, 3, 5], [2, 4, 6]])
            }
        )
        groups.append(group)
    print(f"✅ {len(groups)} ta guruh yaratildi/mavjud")

    # 8. O'QUVCHILAR (30 ta) + OTA-ONALAR
    students = []
    for i in range(30):
        is_male = random.choice([True, False])
        phone = generate_phone()
        student, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                "first_name": random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE),
                "last_name": random.choice(LAST_NAMES),
                "role": "student",
                "organization": org,
                "branch": random.choice(branches),
                "balance": random.choice([0, -500000, -1000000, 500000, 1000000]),
                "profile_data": {
                    "region": "Toshkent shahri",
                    "district": random.choice(["Chilonzor", "Sergeli", "Yunusobod"]),
                    "address": f"Ko'cha #{random.randint(1, 100)}"
                }
            }
        )
        if created:
            student.set_password("student123")
            student.save()
            
            # Ota-ona yaratish
            parent_phone = generate_phone()
            parent, p_created = User.objects.get_or_create(
                phone=parent_phone,
                defaults={
                    "first_name": random.choice(FIRST_NAMES_MALE),
                    "last_name": student.last_name,
                    "role": "parent",
                    "organization": org,
                }
            )
            if p_created:
                parent.set_password(parent_phone[-4:])
                parent.save()
            
            # Bog'liqlik
            ParentStudent.objects.get_or_create(
                parent=parent,
                student=student,
                defaults={
                    "relation_type": random.choice(["father", "mother"]),
                    "is_main_contact": True,
                    "organization": org
                }
            )
        
        students.append(student)
        
        # Guruhga qo'shish
        if created and groups:
            group = random.choice(groups)
            GroupStudent.objects.get_or_create(
                group=group,
                student=student,
                defaults={"status": "active"}
            )
    
    print(f"✅ {len(students)} ta o'quvchi yaratildi/mavjud")

    # 9. CRM - Stages (Voronka bosqichlari)
    stage_names = [
        ("Yangi", "#3B82F6", 1),
        ("Qiziqish bildirdi", "#F59E0B", 2),
        ("Sinov dars", "#8B5CF6", 3),
        ("Shartnoma", "#10B981", 4),
        ("To'lov kutilmoqda", "#EF4444", 5),
    ]
    stages = []
    for name, color, order in stage_names:
        stage, _ = Stage.objects.get_or_create(
            organization=org,
            name=name,
            defaults={"color": color, "order": order}
        )
        stages.append(stage)
    print(f"✅ CRM {len(stages)} ta bosqich yaratildi")

    # 10. Lead Manbalari
    source_names = ["Instagram", "Telegram", "Do'st tavsiyasi", "Banner", "Website"]
    sources = []
    for name in source_names:
        source, _ = LeadSource.objects.get_or_create(
            organization=org,
            name=name
        )
        sources.append(source)
    print(f"✅ {len(sources)} ta manba yaratildi")

    # 11. LIDLAR (20 ta)
    for i in range(20):
        is_male = random.choice([True, False])
        Lead.objects.get_or_create(
            organization=org,
            phone=generate_phone(),
            defaults={
                "full_name": f"{random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}",
                "source": random.choice(sources),
                "stage": random.choice(stages),
            }
        )
    print(f"✅ 20 ta lid yaratildi/mavjud")

    # 12. MOLIYA - Hisoblar
    account_names = [("Asosiy Kassa (Naqd)", "cash"), ("Click/Payme", "online"), ("Bank hisobi", "bank")]
    accounts = []
    for name, acc_type in account_names:
        acc, _ = Account.objects.get_or_create(
            organization=org,
            name=name,
            defaults={"account_type": acc_type, "balance": random.randint(1000000, 50000000)}
        )
        accounts.append(acc)
    print(f"✅ {len(accounts)} ta kassa yaratildi")

    # 13. Kategoriyalar
    categories_data = [
        ("Kurs to'lovi", "income"),
        ("Oylik maosh", "expense"),
        ("Arenda", "expense"),
        ("Kommunal", "expense"),
    ]
    for name, cat_type in categories_data:
        TransactionCategory.objects.get_or_create(
            organization=org,
            name=name,
            defaults={"category_type": cat_type}
        )
    print(f"✅ To'lov kategoriyalari yaratildi")

    print("=" * 50)
    print("✅ BARCHA TEST MA'LUMOTLARI TAYYOR!")
    print("=" * 50)
    print("\n📱 Login ma'lumotlari:")
    print("   Super Admin: 998900000000 / admin")
    print("   O'qituvchi: [telefon] / teacher123")
    print("   O'quvchi: [telefon] / student123")
    print("=" * 50)

if __name__ == "__main__":
    setup()
