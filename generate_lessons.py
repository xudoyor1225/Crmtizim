"""
Guruhlar jadvaliga asoslanib avtomatik darslar yaratish.
Bu script guruhlarning schedule_days maydoniga qarab haftalik darslar yaratadi.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from datetime import date, timedelta, time, datetime
from apps.education.models import Group
from apps.operations.models import Lesson
from django.utils import timezone


def generate_lessons_for_week(start_date=None, weeks_ahead=4):
    """
    Guruhlar uchun darslar yaratish.

    Args:
        start_date: Boshlanish sanasi (default: bugun)
        weeks_ahead: Necha hafta oldinga (default: 4 hafta)
    """
    if start_date is None:
        start_date = date.today()

    # Hafta boshini topish (Dushanba)
    days_since_monday = start_date.weekday()
    week_start = start_date - timedelta(days=days_since_monday)

    print(f"📅 Darslar yaratilmoqda: {week_start} dan {weeks_ahead} hafta oldinga")
    print("=" * 60)

    # Faol guruhlarni olish
    groups = Group.objects.filter(
        is_deleted=False,
        status__in=['active', 'pending']
    ).select_related('teacher', 'room', 'organization')

    if not groups.exists():
        print("❌ Faol guruhlar topilmadi!")
        return

    print(f"✅ {groups.count()} ta guruh topildi\n")

    created_count = 0
    skipped_count = 0

    # Har bir guruh uchun
    for group in groups:
        print(f"\n🎓 Guruh: {group.name}")
        print(f"   O'qituvchi: {group.teacher}")
        print(f"   Dars kunlari: {group.schedule_days}")
        print(f"   Vaqt: {group.start_time} - {group.end_time}")

        if not group.schedule_days:
            print(f"   ⚠️  O'tkazildi: dars kunlari belgilanmagan")
            continue

        if not group.start_time or not group.end_time:
            print(f"   ⚠️  O'tkazildi: vaqt belgilanmagan")
            continue

        # Har bir hafta uchun
        for week in range(weeks_ahead):
            current_week_start = week_start + timedelta(weeks=week)

            # Har bir kun uchun (1-7: Dushanba-Yakshanba)
            for day_number in group.schedule_days:
                # day_number: 1=Dushanba, 2=Seshanba, ..., 7=Yakshanba
                # weekday(): 0=Dushanba, 1=Seshanba, ..., 6=Yakshanba
                lesson_date = current_week_start + timedelta(days=day_number - 1)

                # Agar o'tmishda bo'lsa, o'tkazib yuborish
                if lesson_date < date.today():
                    continue

                # Agar dars allaqachon mavjud bo'lsa, o'tkazib yuborish
                existing = Lesson.objects.filter(
                    group=group,
                    date=lesson_date,
                    start_time=group.start_time,
                    is_deleted=False
                ).exists()

                if existing:
                    skipped_count += 1
                    continue

                # Yangi dars yaratish
                lesson = Lesson.objects.create(
                    organization=group.organization,
                    group=group,
                    teacher=group.teacher,
                    room=group.room,
                    date=lesson_date,
                    start_time=group.start_time,
                    end_time=group.end_time,
                    status='scheduled'
                )

                print(f"   ✅ Yaratildi: {lesson_date} ({lesson.start_time})")
                created_count += 1

    print("\n" + "=" * 60)
    print(f"🎉 Yakunlandi!")
    print(f"   ✅ Yaratildi: {created_count} ta dars")
    print(f"   ⏭️  O'tkazildi: {skipped_count} ta (allaqachon mavjud)")
    print("=" * 60)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        weeks = int(sys.argv[1])
        generate_lessons_for_week(weeks_ahead=weeks)
    else:
        generate_lessons_for_week()
