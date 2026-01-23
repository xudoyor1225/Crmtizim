from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.operations.models import Lesson, Attendance
from apps.finance.models import Transaction, Account, TransactionCategory
from apps.users.models import User


@transaction.atomic
def finish_lesson_logic(lesson_id, user):
    """
    O'qituvchi "Darsni tugatish" tugmasini bosganda ishlaydi.
    1. Statusni 'finished' qiladi.
    2. Kelgan o'quvchilardan pul yechadi.
    3. O'qituvchiga KPI yozadi (keyinchalik).
    """
    try:
        lesson = Lesson.objects.select_for_update().get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise ValidationError("Dars topilmadi")

    if lesson.status == 'finished':
        raise ValidationError("Bu dars allaqachon yakunlangan va pullar yechilgan.")

    # 1. Dars narxini aniqlaymiz (Kurs narxidan kelib chiqib yoki bitta dars narxi)
    # Oddiylik uchun: Oylik narx / 12 ta dars deb olamiz (yoki soatbay)
    # Hozircha statik: 50,000 so'm (Keyin Course modelidan olamiz)
    lesson_price = 50000
    if lesson.group.course.price > 0:
        # Taxminiy hisob: Kurs narxi / 12 dars
        lesson_price = lesson.group.course.price / 12

    # 2. Kategoriyani topamiz (Kurs to'lovi)
    category, _ = TransactionCategory.objects.get_or_create(
        organization=lesson.organization,
        transaction_type='income',
        defaults={'name': 'Kurs to\'lovi avtomat'}
    )

    # 3. Davomatni tekshiramiz
    attendances = Attendance.objects.filter(lesson=lesson)

    if not attendances.exists():
        raise ValidationError("Davomat qilinmagan! Avval o'quvchilarni belgilang.")

    for att in attendances:
        # Agar o'quvchi BOR bo'lsa yoki SABABSIZ yo'q bo'lsa -> Pul yechamiz
        if att.status in ['present', 'late', 'absent']:
            # Tranzaksiya yaratamiz (Avtomatik tasdiqlangan holda)
            # Chunki bu real balansdan yechilyapti

            Transaction.objects.create(
                organization=lesson.organization,
                branch=lesson.group.room.organization.branches.first() if lesson.room else None,  # Vaqtincha logic
                account=Account.objects.filter(organization=lesson.organization).first(),  # Virtual hisob
                category=category,
                student=att.student,
                amount=lesson_price,
                transaction_type='income',  # Aslida bu "Realizatsiya", balansdan kamayishi kerak.
                # DIQQAT: Bu yerda logika shunday:
                # Student balansidan pul kamayadi -> Markaz foydasiga yoziladi.
                # Sodda bo'lishi uchun: Biz shunchaki student balansini kamaytiramiz.
                status='confirmed',
                created_by=user,
                confirmed_by=user,
                confirmed_at=timezone.now(),
                description=f"{lesson.group.name} - {lesson.date} darsi uchun to'lov"
            )

            # O'quvchi balansini kamaytiramiz
            att.student.balance -= lesson_price
            att.student.save()

    # 4. Darsni yopamiz
    lesson.status = 'finished'
    lesson.finished_at = timezone.now()
    lesson.save()

    return "Dars yakunlandi va hisob-kitob qilindi."