"""
Rol asosli Dashboard viewlari.
Har bir rol uchun alohida ma'lumotlar va statistikalar.
Cache bilan optimizatsiya qilingan.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta

from apps.users.models import User, ParentStudent
from apps.organizations.models import Organization, Branch
from apps.crm.models import Lead, Stage
from apps.education.models import Course, Group, GroupStudent
from apps.operations.models import Lesson, Attendance
from apps.finance.models import Transaction, Account


def get_date_range(days=30):
    """So'nggi N kun uchun sana oralig'ini qaytaradi."""
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def get_cached_or_compute(cache_key, compute_func, timeout=300):
    """
    Cache dan olish yoki hisoblash.
    Args:
        cache_key: Cache kaliti
        compute_func: Cache topilmasa chaqiriladigan funksiya
        timeout: Cache muddati (soniyalarda)
    """
    result = cache.get(cache_key)
    if result is None:
        result = compute_func()
        cache.set(cache_key, result, timeout)
    return result


@login_required
def role_based_dashboard(request):
    """
    Foydalanuvchi roliga qarab tegishli dashboardga yo'naltiradi.
    """
    user = request.user
    role = user.role
    
    if role == 'super_admin':
        return super_admin_dashboard(request)
    elif role in ['owner', 'admin']:
        return admin_dashboard(request)
    elif role == 'teacher':
        return teacher_dashboard(request)
    elif role == 'student':
        return student_dashboard(request)
    elif role == 'parent':
        return parent_dashboard(request)
    else:
        return staff_dashboard(request)


@login_required
def super_admin_dashboard(request):
    """
    Super Admin uchun - butun tizim statistikasi.
    Moliya, O'quvchilar, Qarzdorlik, Bildirishnomalar - barcha muhim ma'lumotlar.
    """
    from django.db.models import F
    from apps.finance.inventory import Supply
    
    today = timezone.now().date()
    
    # ====== HAFTALIK/OYLIK TOGGLE ======
    period = request.GET.get('period', 'monthly')
    if period == 'weekly':
        start_date, end_date = get_date_range(7)
        period_label = "Haftalik"
    else:
        start_date, end_date = get_date_range(30)
        period_label = "Oylik"
    
    # ====== TASHKILOTLAR ======
    total_orgs = Organization.objects.filter(is_deleted=False).count()
    active_orgs = Organization.objects.filter(is_deleted=False, is_active=True).count()
    
    # ====== FOYDALANUVCHILAR ======
    total_users = User.objects.filter(is_active=True).count()
    users_by_role = User.objects.filter(is_active=True).values('role').annotate(count=Count('id'))
    users_by_role_dict = {item['role']: item['count'] for item in users_by_role}
    
    # O'quvchilar statistikasi
    total_students = users_by_role_dict.get('student', 0)
    active_students = User.objects.filter(role='student', is_active=True, is_deleted=False).count()
    frozen_students = GroupStudent.objects.filter(status='frozen').values('student').distinct().count()
    
    # ====== BUGUNGI STATISTIKA ======
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_leads_today = Lead.objects.filter(created_at__date=today).count()
    
    # ====== MOLIYA (BARCHA TASHKILOTLAR BO'YICHA) ======
    today_income = Transaction.objects.filter(
        transaction_type='income',
        status='confirmed',
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    today_expense = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed', 
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Davr bo'yicha (haftalik/oylik)
    period_income = Transaction.objects.filter(
        transaction_type='income',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    period_expense = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_profit = period_income - period_expense
    
    # ====== KUNLIK XARAJATLAR TAQSIMOTI ======
    daily_expenses = Transaction.objects.filter(
        transaction_type='expense',
        status='confirmed',
        created_at__date=today
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    # ====== QARZDORLIK ======
    debtors = User.objects.filter(role='student', balance__lt=0, is_active=True)
    total_debt = abs(debtors.aggregate(total=Sum('balance'))['total'] or 0)
    debtors_count = debtors.count()
    
    # ====== TUG'ILGAN KUNLAR ======
    today_birthdays = User.objects.filter(
        is_active=True,
        birth_date__month=today.month,
        birth_date__day=today.day
    ).select_related('organization')[:10]
    
    # ====== DAVOMAT (BUGUNGI) ======
    today_lessons = Lesson.objects.filter(date=today)
    total_today_lessons = today_lessons.count()
    finished_lessons = today_lessons.filter(status='finished').count()
    
    # O'quvchilar davomati foizi
    today_attendance = Attendance.objects.filter(lesson__date=today)
    total_attendances = today_attendance.count()
    present_count = today_attendance.filter(status='present').count()
    attendance_rate = (present_count / total_attendances * 100) if total_attendances > 0 else 0
    
    # ====== GURUHLAR ======
    total_groups = Group.objects.filter(is_deleted=False).count()
    active_groups = Group.objects.filter(status='active', is_deleted=False).count()
    
    # ====== OXIRGI HARAKATLAR ======
    recent_orgs = Organization.objects.filter(is_deleted=False).order_by('-created_at')[:5]
    recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:10]
    recent_transactions = Transaction.objects.filter(status='confirmed').order_by('-created_at')[:5]
    
    # ====== KUTILAYOTGAN TO'LOVLAR (Tasdiqlanmagan) ======
    pending_payments = Transaction.objects.filter(
        status='pending',
        transaction_type='income'
    ).count()
    
    # ====== TASDIQLANMAGAN CHEKLAR ======
    pending_receipts = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).count()
    pending_receipts_sum = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).aggregate(total=Sum('amount'))['total'] or 0
    pending_receipts_list = Transaction.objects.filter(
        status='pending',
        receipt_verified=False,
        payment_method__in=['card', 'transfer', 'online']
    ).select_related('student', 'created_by').order_by('-created_at')[:5]
    
    # ====== KAM QOLGAN MAHSULOTLAR (SKLAD) ======
    low_stock_items = Supply.objects.filter(
        is_deleted=False,
        quantity__lte=F('min_quantity')
    )[:10]
    low_stock_count = Supply.objects.filter(
        is_deleted=False,
        quantity__lte=F('min_quantity')
    ).count()
    
    context = {
        # Tashkilotlar
        'total_orgs': total_orgs,
        'active_orgs': active_orgs,
        
        # Foydalanuvchilar
        'total_users': total_users,
        'users_by_role': users_by_role_dict,
        'total_students': total_students,
        'active_students': active_students,
        'frozen_students': frozen_students,
        
        # Bugungi
        'new_users_today': new_users_today,
        'new_leads_today': new_leads_today,
        
        # Moliya (haftalik/oylik toggle)
        'period': period,
        'period_label': period_label,
        'today_income': today_income,
        'today_expense': today_expense,
        'period_income': period_income,
        'period_expense': period_expense,
        'net_profit': net_profit,
        'daily_expenses': daily_expenses,
        
        # Qarzdorlik
        'total_debt': total_debt,
        'debtors_count': debtors_count,
        
        # Tug'ilgan kunlar
        'today_birthdays': today_birthdays,
        
        # Davomat
        'total_today_lessons': total_today_lessons,
        'finished_lessons': finished_lessons,
        'attendance_rate': round(attendance_rate, 1),
        
        # Guruhlar
        'total_groups': total_groups,
        'active_groups': active_groups,
        
        # Oxirgi harakatlar
        'recent_orgs': recent_orgs,
        'recent_users': recent_users,
        'recent_transactions': recent_transactions,
        
        # Bildirishnomalar
        'pending_payments': pending_payments,
        'pending_receipts': pending_receipts,
        'pending_receipts_sum': pending_receipts_sum,
        'pending_receipts_list': pending_receipts_list,
        'low_stock_items': low_stock_items,
        'low_stock_count': low_stock_count,
        'today': today,
    }
    
    return render(request, 'dashboards/super_admin.html', context)


@login_required
def admin_dashboard(request):
    """
    Admin/Owner uchun - o'z tashkiloti statistikasi.
    """
    org = request.user.organization
    
    # O'quvchilar
    total_students = User.objects.filter(
        organization=org, role='student', is_active=True, is_deleted=False
    ).count()
    
    # O'qituvchilar
    total_teachers = User.objects.filter(
        organization=org, role='teacher', is_active=True, is_deleted=False
    ).count()
    
    # Guruhlar
    active_groups = Group.objects.filter(
        organization=org, status='active', is_deleted=False
    ).count()
    
    # Lidlar
    total_leads = Lead.objects.filter(organization=org, is_deleted=False).count()
    new_leads = Lead.objects.filter(
        organization=org, 
        is_deleted=False,
        created_at__date=timezone.now().date()
    ).count()
    
    # Moliya
    start_date, end_date = get_date_range(30)
    monthly_income = Transaction.objects.filter(
        organization=org,
        transaction_type='income',
        status='confirmed',
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Qarzdorlik
    total_debt = User.objects.filter(
        organization=org, role='student', balance__lt=0
    ).aggregate(total=Sum('balance'))['total'] or 0
    
    # Bugungi darslar
    today_lessons = Lesson.objects.filter(
        organization=org,
        date=timezone.now().date()
    ).select_related('group', 'teacher', 'room').order_by('start_time')[:10]
    
    # So'nggi lidlar
    recent_leads = Lead.objects.filter(
        organization=org, is_deleted=False
    ).select_related('source', 'stage').order_by('-created_at')[:5]
    
    # Voronka bosqichlari
    stages = Stage.objects.filter(organization=org).annotate(
        lead_count=Count('leads', filter=Q(leads__is_deleted=False))
    ).order_by('order')
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'active_groups': active_groups,
        'total_leads': total_leads,
        'new_leads': new_leads,
        'monthly_income': monthly_income,
        'total_debt': abs(total_debt),
        'today_lessons': today_lessons,
        'recent_leads': recent_leads,
        'stages': stages,
    }
    
    return render(request, 'dashboards/admin.html', context)


@login_required
def teacher_dashboard(request):
    """
    O'qituvchi uchun - o'z guruhlari va darslari.
    KPI statistikasi va reyting bilan.
    """
    from django.db.models import Avg
    
    teacher = request.user
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # Mening guruhlarim
    my_groups = Group.objects.filter(
        teacher=teacher, 
        status__in=['active', 'pending'],
        is_deleted=False
    ).select_related('course', 'room').annotate(
        student_count=Count('students', filter=Q(students__status='active'))
    )
    
    # Bugungi darslarim
    today_lessons = Lesson.objects.filter(
        teacher=teacher,
        date=today
    ).select_related('group', 'room').order_by('start_time')
    
    # Keyingi darslarim (5 kun)
    upcoming_lessons = Lesson.objects.filter(
        teacher=teacher,
        date__gt=today,
        date__lte=today + timedelta(days=5)
    ).select_related('group', 'room').order_by('date', 'start_time')[:10]
    
    # O'tkazilmagan darslar (davomat belgilanmagan)
    pending_attendance = Lesson.objects.filter(
        teacher=teacher,
        date__lte=today,
        status='scheduled'
    ).select_related('group').order_by('-date')[:5]
    
    # Umumiy statistika
    total_students = GroupStudent.objects.filter(
        group__teacher=teacher,
        group__status='active',
        status='active'
    ).count()
    
    # ====== KPI STATISTIKASI ======
    # Oylik darslar
    monthly_lessons = Lesson.objects.filter(
        teacher=teacher,
        date__gte=start_of_month,
        date__lte=today
    )
    total_monthly_lessons = monthly_lessons.count()
    completed_lessons = monthly_lessons.filter(status='finished').count()
    lesson_completion_rate = (completed_lessons / total_monthly_lessons * 100) if total_monthly_lessons > 0 else 0
    
    # O'quvchilar davomati (mening darslarimda)
    my_lesson_ids = monthly_lessons.values_list('id', flat=True)
    monthly_attendance = Attendance.objects.filter(lesson_id__in=my_lesson_ids)
    total_attendance_records = monthly_attendance.count()
    present_records = monthly_attendance.filter(status='present').count()
    student_attendance_rate = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0
    
    # O'rtacha baho (bergan baholarim)
    avg_grade_given = monthly_attendance.filter(
        grade__isnull=False
    ).aggregate(avg=Avg('grade'))['avg'] or 0
    
    # XP berilgani
    total_xp_given = monthly_attendance.aggregate(
        total=Sum('xp_points')
    )['total'] or 0
    
    context = {
        'my_groups': my_groups,
        'today_lessons': today_lessons,
        'upcoming_lessons': upcoming_lessons,
        'pending_attendance': pending_attendance,
        'total_students': total_students,
        'today': today,
        # KPI
        'total_monthly_lessons': total_monthly_lessons,
        'completed_lessons': completed_lessons,
        'lesson_completion_rate': round(lesson_completion_rate, 1),
        'student_attendance_rate': round(student_attendance_rate, 1),
        'avg_grade_given': round(avg_grade_given, 1),
        'total_xp_given': total_xp_given,
    }
    
    return render(request, 'dashboards/teacher.html', context)


@login_required
def student_dashboard(request):
    """
    O'quvchi uchun - dars jadvali, baholar, to'lovlar.
    Leaderboard va gamifikatsiya bilan.
    """
    from apps.operations.shop import ShopItem
    
    student = request.user
    today = timezone.now().date()
    
    # Mening guruhlarim
    my_enrollments = GroupStudent.objects.filter(
        student=student,
        status='active'
    ).select_related('group', 'group__course', 'group__teacher', 'group__room')
    
    my_groups = [e.group for e in my_enrollments]
    
    # Bugungi darslarim
    today_lessons = Lesson.objects.filter(
        group__in=my_groups,
        date=today
    ).select_related('group', 'teacher', 'room').order_by('start_time')
    
    # Keyingi darslar
    upcoming_lessons = Lesson.objects.filter(
        group__in=my_groups,
        date__gt=today
    ).select_related('group', 'teacher', 'room').order_by('date', 'start_time')[:10]
    
    # Davomatim
    my_attendance = Attendance.objects.filter(
        student=student
    ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:20]
    
    # Statistikalar
    total_lessons = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='present').count()
    attendance_rate = (present_count / total_lessons * 100) if total_lessons > 0 else 0
    
    # Baholar o'rtachasi
    grades = Attendance.objects.filter(
        student=student, 
        grade__isnull=False
    ).values_list('grade', flat=True)
    avg_grade = sum(grades) / len(grades) if grades else 0
    
    # XP (Attendance dan)
    total_xp = Attendance.objects.filter(student=student).aggregate(
        total=Sum('xp_points')
    )['total'] or 0
    
    # Coin (profile_data dan yoki XP dan)
    coin_balance = student.profile_data.get('xp', total_xp) if hasattr(student, 'profile_data') and student.profile_data else total_xp
    
    # Balans
    balance = student.balance
    
    # To'lovlar tarixi
    payments = Transaction.objects.filter(
        student=student
    ).order_by('-created_at')[:10]

    # Chart Data (So'nggi 10 ta baho)
    grade_history = Attendance.objects.filter(
        student=student, 
        grade__isnull=False
    ).select_related('lesson').order_by('lesson__date')
    
    # Oxirgi 10 tasini olib, keyin sana bo'yicha tartiblaymiz
    grade_history = list(grade_history)[-10:]
    
    chart_labels = [att.lesson.date.strftime('%d.%m') for att in grade_history]
    chart_data = [att.grade for att in grade_history]
    
    # ====== LEADERBOARD (Top 10 XP bo'yicha) ======
    # O'quvchining tashkilotidagi eng ko'p XP yig'ganlar
    org = student.organization
    leaderboard = User.objects.filter(
        role='student',
        organization=org,
        is_active=True,
        is_deleted=False
    ).annotate(
        xp_total=Sum('lesson_attendances__xp_points')
    ).exclude(xp_total__isnull=True).order_by('-xp_total')[:10]
    
    # O'quvchining reytingdagi o'rni
    student_rank = 0
    for i, s in enumerate(leaderboard, 1):
        if s.id == student.id:
            student_rank = i
            break
    
    # ====== SHOP ======
    shop_items_count = ShopItem.objects.filter(
        organization=org,
        is_active=True,
        is_deleted=False
    ).count() if org else 0
    
    context = {
        'my_enrollments': my_enrollments,
        'today_lessons': today_lessons,
        'upcoming_lessons': upcoming_lessons,
        'my_attendance': my_attendance,
        'attendance_rate': round(attendance_rate, 1),
        'avg_grade': round(avg_grade, 1),
        'total_xp': total_xp,
        'coin_balance': coin_balance,
        'balance': balance,
        'payments': payments,
        'today': today,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        # Leaderboard
        'leaderboard': leaderboard,
        'student_rank': student_rank,
        # Shop
        'shop_items_count': shop_items_count,
    }
    
    return render(request, 'dashboards/student.html', context)


@login_required
def parent_dashboard(request):
    """
    Ota-ona uchun - farzandlari haqida ma'lumot.
    """
    parent = request.user
    today = timezone.now().date()
    
    # Farzandlarim
    children_relations = ParentStudent.objects.filter(
        parent=parent
    ).select_related('student')
    
    children_data = []
    
    for relation in children_relations:
        child = relation.student
        
        # O'quvchining guruhlari
        enrollments = GroupStudent.objects.filter(
            student=child,
            status='active'
        ).select_related('group', 'group__course', 'group__teacher')
        
        # Davomat statistikasi
        total_att = Attendance.objects.filter(student=child).count()
        present = Attendance.objects.filter(student=child, status='present').count()
        att_rate = (present / total_att * 100) if total_att > 0 else 0
        
        # O'rtacha baho
        grades = Attendance.objects.filter(
            student=child, grade__isnull=False
        ).values_list('grade', flat=True)
        avg_grade = sum(grades) / len(grades) if grades else 0
        
        # So'nggi davomatlar
        recent_attendance = Attendance.objects.filter(
            student=child
        ).select_related('lesson', 'lesson__group').order_by('-lesson__date')[:5]
        
        children_data.append({
            'child': child,
            'relation_type': relation.get_relation_type_display(),
            'enrollments': enrollments,
            'attendance_rate': round(att_rate, 1),
            'avg_grade': round(avg_grade, 1),
            'balance': child.balance,
            'has_debt': child.balance < 0,
            'xp': Attendance.objects.filter(student=child).aggregate(total=Sum('xp_points'))['total'] or 0,
            'recent_attendance': recent_attendance,
        })
    
    # Umumiy qarzdorlik
    total_debt = sum(abs(d['balance']) for d in children_data if d['has_debt'])
    has_any_debt = any(d['has_debt'] for d in children_data)
    
    context = {
        'children_data': children_data,
        'today': today,
        'total_debt': total_debt,
        'has_any_debt': has_any_debt,
    }
    
    return render(request, 'dashboards/parent.html', context)


@login_required
def staff_dashboard(request):
    """
    Oddiy xodim uchun - umumiy ma'lumotlar.
    """
    context = {
        'user': request.user,
    }
    return render(request, 'dashboards/staff.html', context)
