"""
Operations views - Darslar va Davomat tizimi (ASYNC optimized).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Avg
from datetime import timedelta
from asgiref.sync import sync_to_async

from .models import Lesson, Attendance
from apps.education.models import Group, GroupStudent
from apps.users.models import User
from apps.core.audit import log_user_action


# Shablon izohlar - davomat olishda tez tanlash uchun
ATTENDANCE_NOTES = [
    "Darsga tayyor",
    "Uy vazifasini bajargan",
    "Faol qatnashdi",
    "Diqqat bilan tingladi",
    "Savollar berdi",
    "Uy vazifasini bajarmagan",
    "Darsga kech keldi",
    "Telefonni ko'p ishlatdi",
    "Sababli kelmadi - kasal",
    "Sababli kelmadi - oilaviy",
]


# Async helper functions
@sync_to_async
def get_lessons_data(user, org, date_filter, group_filter, status_filter):
    """Darslar ma'lumotlarini async olish"""
    # Super admin barcha darslarni ko'radi
    if user.role == 'super_admin' or not org:
        lessons = Lesson.objects.filter(is_deleted=False)
    else:
        lessons = Lesson.objects.filter(organization=org, is_deleted=False)

    # Agar o'qituvchi bo'lsa, faqat o'z darslari
    if user.role == 'teacher':
        lessons = lessons.filter(teacher=user)
    
    if date_filter:
        lessons = lessons.filter(date=date_filter)
    if group_filter:
        lessons = lessons.filter(group_id=group_filter)
    if status_filter:
        lessons = lessons.filter(status=status_filter)
    
    lessons = lessons.select_related('group', 'teacher', 'room').prefetch_related('attendances').order_by('start_time')
    
    # Davomat olinganligini tekshirish
    lessons_data = []
    for lesson in lessons:
        attendance_count = lesson.attendances.count()
        lessons_data.append({
            'lesson': lesson,
            'attendance_taken': attendance_count > 0,
            'attendance_count': attendance_count,
            'present_count': lesson.attendances.filter(status='present').count(),
        })
    
    return lessons_data, list(lessons)


@sync_to_async
def get_groups_for_filter(user, org):
    """Guruhlarni filter uchun olish"""
    if user.role == 'teacher':
        groups = Group.objects.filter(teacher=user, is_deleted=False)
    elif user.role == 'super_admin' or not org:
        groups = Group.objects.filter(is_deleted=False)
    else:
        groups = Group.objects.filter(organization=org, is_deleted=False)
    return list(groups)


# ===========================================
# LESSONS (DARSLAR)
# ===========================================

@login_required
def lesson_list(request):
    """Darslar va Jadval - birlashtirilgan dashboard"""
    org = request.user.organization
    user = request.user
    today = timezone.now().date()

    # Filter parametrlari
    date_filter = request.GET.get('date', str(today))
    group_filter = request.GET.get('group', '')
    status_filter = request.GET.get('status', '')

    # Super admin barcha darslarni ko'radi
    if user.role == 'super_admin' or not org:
        lessons = Lesson.objects.filter(is_deleted=False)
    else:
        lessons = Lesson.objects.filter(organization=org, is_deleted=False)

    # Agar o'qituvchi bo'lsa, faqat o'z darslari
    if user.role == 'teacher':
        lessons = lessons.filter(teacher=user)

    if date_filter:
        lessons = lessons.filter(date=date_filter)
    if group_filter:
        lessons = lessons.filter(group_id=group_filter)
    if status_filter:
        lessons = lessons.filter(status=status_filter)

    lessons = lessons.select_related('group', 'teacher', 'room').prefetch_related('attendances').order_by('start_time')

    # Davomat olinganligini tekshirish
    lessons_data = []
    attendance_taken_count = 0
    ongoing_count = 0
    for lesson in lessons:
        attendance_count = lesson.attendances.count()
        if attendance_count > 0:
            attendance_taken_count += 1
        if lesson.status == 'started':
            ongoing_count += 1
        lessons_data.append({
            'lesson': lesson,
            'attendance_taken': attendance_count > 0,
            'attendance_count': attendance_count,
            'present_count': lesson.attendances.filter(status='present').count(),
        })

    # Guruhlar filter uchun
    if user.role == 'teacher':
        groups = Group.objects.filter(teacher=user, is_deleted=False)
    elif user.role == 'super_admin' or not org:
        groups = Group.objects.filter(is_deleted=False)
    else:
        groups = Group.objects.filter(organization=org, is_deleted=False)

    # ========== HAFTALIK JADVAL ==========
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    week_offset = int(request.GET.get('week', 0))
    start_of_week += timedelta(weeks=week_offset)
    end_of_week += timedelta(weeks=week_offset)

    # Faol guruhlar
    if user.role == 'super_admin' or not org:
        schedule_groups = Group.objects.filter(
            is_deleted=False, status__in=['active', 'pending']
        ).select_related('teacher', 'room', 'course')
    else:
        schedule_groups = Group.objects.filter(
            organization=org, is_deleted=False, status__in=['active', 'pending']
        ).select_related('teacher', 'room', 'course')

    if user.role == 'teacher':
        schedule_groups = schedule_groups.filter(teacher=user)
    elif user.role == 'student':
        my_groups = GroupStudent.objects.filter(student=user, status='active').values_list('group_id', flat=True)
        schedule_groups = schedule_groups.filter(id__in=my_groups)

    # Hafta kunlari
    day_names = ['', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
    week_days = []
    weekly_lessons_count = 0

    for i in range(7):
        day_number = i + 1
        day_date = start_of_week + timedelta(days=i)
        day_groups = []

        for group in schedule_groups:
            if group.schedule_days and day_number in group.schedule_days:
                weekly_lessons_count += 1
                day_groups.append({
                    'group': group,
                    'name': group.name,
                    'start_time': group.start_time,
                    'end_time': group.end_time,
                    'room': group.room,
                    'teacher': group.teacher,
                })

        day_groups.sort(key=lambda x: x['start_time'] if x['start_time'] else timezone.now().time())

        week_days.append({
            'day_number': day_number,
            'day_name': day_names[day_number],
            'date': day_date,
            'is_today': day_date == today,
            'groups': day_groups,
        })

    context = {
        # Bugungi darslar
        'lessons_data': lessons_data,
        'lessons': lessons,
        'groups': groups,
        'today': today,
        'date_filter': date_filter,
        'group_filter': group_filter,
        'status_filter': status_filter,
        # Statistika
        'today_lessons_count': len(lessons_data),
        'attendance_taken_count': attendance_taken_count,
        'ongoing_count': ongoing_count,
        'weekly_lessons_count': weekly_lessons_count,
        # Haftalik jadval
        'week_days': week_days,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_offset': week_offset,
    }
    
    return render(request, 'operations/lessons_dashboard.html', context)


@login_required
def lesson_add(request):
    """Yangi dars qo'shish"""
    org = request.user.organization
    user = request.user
    
    # Faqat admin va o'qituvchilar dars qo'sha oladi
    if user.role not in ['super_admin', 'owner', 'admin', 'teacher']:
        messages.error(request, "Sizda dars qo'shish huquqi yo'q!")
        return redirect('operations:lesson_list')
    
    # Guruhlar va xonalar
    if user.role == 'teacher':
        groups = Group.objects.filter(teacher=user, is_deleted=False, status='active')
    elif user.role == 'super_admin' or not org:
        groups = Group.objects.filter(is_deleted=False, status='active')
    else:
        groups = Group.objects.filter(organization=org, is_deleted=False, status='active')
    
    from apps.education.models import Room
    if user.role == 'super_admin' or not org:
        rooms = Room.objects.filter(is_deleted=False)
    else:
        rooms = Room.objects.filter(organization=org, is_deleted=False)

    if request.method == 'POST':
        group_id = request.POST.get('group')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room_id = request.POST.get('room') or None
        topic = request.POST.get('topic', '')
        
        if group_id and date and start_time and end_time:
            group = get_object_or_404(Group, pk=group_id)
            
            lesson = Lesson.objects.create(
                organization=org or group.organization,
                group=group,
                teacher=group.teacher or user,
                date=date,
                start_time=start_time,
                end_time=end_time,
                room_id=room_id,
                topic=topic,
                status='scheduled'
            )
            
            log_user_action(user, 'CREATE', 'Lesson', lesson.id, str(lesson), request=request)
            messages.success(request, "Dars muvaffaqiyatli qo'shildi!")
            return redirect('operations:lesson_list')
        else:
            messages.error(request, "Barcha maydonlarni to'ldiring!")
    
    context = {
        'groups': groups,
        'rooms': rooms,
        'today': timezone.now().date(),
    }
    
    return render(request, 'operations/lesson_form.html', context)


@login_required
def lesson_detail(request, pk):
    """Dars tafsilotlari"""
    org = request.user.organization
    user = request.user

    # Super admin barcha darslarni ko'radi
    if user.role == 'super_admin' or not org:
        lesson = get_object_or_404(Lesson, pk=pk, is_deleted=False)
    else:
        lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)

    # Ushbu darsdagi davomatlar
    attendances = Attendance.objects.filter(lesson=lesson).select_related('student')
    
    context = {
        'lesson': lesson,
        'attendances': attendances,
    }
    
    return render(request, 'operations/lesson_detail.html', context)


@login_required
def start_lesson(request, pk):
    """Darsni boshlash"""
    org = request.user.organization
    user = request.user

    # Super admin barcha darslarni boshlashi mumkin
    if user.role == 'super_admin' or not org:
        lesson = get_object_or_404(Lesson, pk=pk, is_deleted=False)
    else:
        lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)

    if lesson.status == 'scheduled':
        lesson.status = 'started'
        lesson.started_at = timezone.now()
        lesson.save()
        log_user_action(request.user, 'UPDATE', 'Lesson', lesson.id, str(lesson), 
                       changes={'status': 'started'}, request=request)
        messages.success(request, "Dars boshlandi!")
    
    return redirect('operations:take_attendance', pk=lesson.pk)


@login_required
def finish_lesson(request, pk):
    """Darsni yakunlash"""
    org = request.user.organization
    user = request.user

    # Super admin barcha darslarni yakunlashi mumkin
    if user.role == 'super_admin' or not org:
        lesson = get_object_or_404(Lesson, pk=pk, is_deleted=False)
    else:
        lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)

    if lesson.status in ['scheduled', 'started']:
        lesson.status = 'finished'
        lesson.finished_at = timezone.now()
        lesson.save()
        log_user_action(request.user, 'UPDATE', 'Lesson', lesson.id, str(lesson), 
                       changes={'status': 'finished'}, request=request)
        messages.success(request, "Dars yakunlandi!")
    
    return redirect('operations:lesson_list')


# ===========================================
# ATTENDANCE (DAVOMAT)
# ===========================================

@login_required
def take_attendance(request, pk):
    """Davomat olish sahifasi"""
    org = request.user.organization
    user = request.user

    # Super admin barcha darslarni ko'radi
    if user.role == 'super_admin' or not org:
        lesson = get_object_or_404(Lesson, pk=pk, is_deleted=False)
    else:
        lesson = get_object_or_404(Lesson, pk=pk, organization=org, is_deleted=False)

    # Guruhdagi o'quvchilar
    group_students = GroupStudent.objects.filter(
        group=lesson.group,
        status='active'
    ).select_related('student')
    
    # Mavjud davomatlar
    existing_attendances = {
        att.student_id: att 
        for att in Attendance.objects.filter(lesson=lesson)
    }
    
    if request.method == 'POST':
        for gs in group_students:
            student = gs.student
            status = request.POST.get(f'status_{student.id}', 'absent')
            grade = request.POST.get(f'grade_{student.id}', '')
            comment = request.POST.get(f'comment_{student.id}', '')
            
            # XP hisoblash
            xp = 0
            if status == 'present':
                xp = 10
            elif status == 'late':
                xp = 5
            elif status == 'excused':
                xp = 3
            
            # Mavjud davomatni yangilash yoki yangi yaratish
            if student.id in existing_attendances:
                att = existing_attendances[student.id]
                att.status = status
                att.grade = int(grade) if grade else None
                att.comment = comment
                att.xp_points = xp
                att.save()
            else:
                Attendance.objects.create(
                    organization=org or lesson.organization,
                    lesson=lesson,
                    student=student,
                    status=status,
                    grade=int(grade) if grade else None,
                    comment=comment,
                    xp_points=xp,
                )
        
        log_user_action(request.user, 'UPDATE', 'Attendance', lesson.id, 
                       f"Davomat - {lesson.group.name}", request=request)
        messages.success(request, "Davomat saqlandi!")
        return redirect('operations:lesson_list')

    # O'quvchilar ro'yxatini tayyorlash
    students_data = []
    for gs in group_students:
        existing = existing_attendances.get(gs.student_id)
        students_data.append({
            'student': gs.student,
            'status': existing.status if existing else 'present',
            'grade': existing.grade if existing else None,
            'comment': existing.comment if existing else '',
        })
    
    context = {
        'lesson': lesson,
        'students_data': students_data,
    }
    
    return render(request, 'operations/take_attendance.html', context)


# ===========================================
# SCHEDULE (JADVAL)
# ===========================================

@login_required
def schedule_view(request):
    """Haftalik jadval - lesson_list ga redirect"""
    return redirect('operations:lesson_list')


# ===========================================
# RATINGS (REYTINGLAR)
# ===========================================

@login_required
def teacher_ratings(request):
    """O'qituvchilar reytingi"""
    org = request.user.organization
    
    teachers = User.objects.filter(
        organization=org,
        role='teacher',
        is_deleted=False
    ).annotate(
        group_count=Count('teaching_groups', filter=Q(teaching_groups__status='active')),
        student_count=Count(
            'teaching_groups__students',
            filter=Q(teaching_groups__status='active', teaching_groups__students__status='active')
        ),
        lesson_count=Count('lesson', filter=Q(lesson__status='finished')),
    ).order_by('-student_count')
    
    # O'rtacha davomat hisoblash
    teachers_data = []
    for teacher in teachers:
        # O'rtacha davomat foizi
        total_att = Attendance.objects.filter(
            lesson__teacher=teacher,
            lesson__status='finished'
        ).count()
        present_att = Attendance.objects.filter(
            lesson__teacher=teacher,
            lesson__status='finished',
            status='present'
        ).count()
        att_rate = (present_att / total_att * 100) if total_att > 0 else 0
        
        # O'rtacha baho
        avg_grade = Attendance.objects.filter(
            lesson__teacher=teacher,
            grade__isnull=False
        ).aggregate(avg=Avg('grade'))['avg'] or 0
        
        teachers_data.append({
            'teacher': teacher,
            'group_count': teacher.group_count,
            'student_count': teacher.student_count,
            'lesson_count': teacher.lesson_count,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
        })
    
    return render(request, 'operations/teacher_ratings.html', {'teachers_data': teachers_data})


@login_required
def student_ratings(request):
    """O'quvchilar reytingi (Leaderboard)"""
    org = request.user.organization
    
    students = User.objects.filter(
        organization=org,
        role='student',
        is_deleted=False
    )
    
    students_data = []
    for student in students:
        # Davomat
        total_att = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='present').count()
        att_rate = (present / total_att * 100) if total_att > 0 else 0
        
        # O'rtacha baho
        avg_grade = Attendance.objects.filter(
            student=student,
            grade__isnull=False
        ).aggregate(avg=Avg('grade'))['avg'] or 0
        
        # Jami XP
        total_xp = Attendance.objects.filter(student=student).aggregate(
            total=Count('xp_points')
        )['total'] or 0
        
        # Guruhlar soni
        group_count = GroupStudent.objects.filter(
            student=student, status='active'
        ).count()
        
        students_data.append({
            'student': student,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
            'total_xp': total_xp,
            'group_count': group_count,
            # Umumiy ball (reyting uchun)
            'score': round(att_rate * 0.3 + avg_grade * 0.5 + total_xp * 0.2, 1)
        })
    
    # Baliga ko'ra tartiblash
    students_data.sort(key=lambda x: x['score'], reverse=True)
    
    # Rank qo'shish
    for i, data in enumerate(students_data):
        data['rank'] = i + 1
    
    return render(request, 'operations/student_ratings.html', {'students_data': students_data})
