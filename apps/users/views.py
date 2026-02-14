from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db import transaction
from asgiref.sync import sync_to_async
from .models import User, ParentStudent
from .forms import UserForm, StudentForm, TeacherForm, StaffForm
from apps.core.permissions import permission_required, check_permission


# Async helper functions
@sync_to_async
def get_users_data(user, role, filter_type, search, page):
    """Users ma'lumotlarini async olish"""
    users = User.objects.filter(is_deleted=False).select_related('organization', 'branch').order_by('-date_joined')

    if user.role != 'super_admin' and user.organization:
        users = users.filter(organization=user.organization)

    if role:
        users = users.filter(role=role)

    if filter_type == 'debtors':
        users = users.filter(role='student', balance__lt=0)

    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )

    # Statistika
    base_qs = User.objects.filter(is_deleted=False)
    if user.role != 'super_admin' and user.organization:
        base_qs = base_qs.filter(organization=user.organization)

    total_students = base_qs.filter(role='student', is_active=True).count()
    debtors_count = base_qs.filter(role='student', balance__lt=0).count()
    debt_agg = base_qs.filter(role='student', balance__lt=0).aggregate(total=Sum('balance'))
    total_debt = abs(debt_agg['total'] or 0)

    # Pagination
    paginator = Paginator(users, 25)
    users_page = paginator.get_page(page)

    return users_page, total_students, debtors_count, total_debt


@login_required
@permission_required('users', 'view')
async def user_list(request, role=None):
    """Foydalanuvchilar ro'yxati (ASYNC)"""
    if not role:
        role = request.GET.get('role')
    filter_type = request.GET.get('filter')
    search = request.GET.get('q')
    page = request.GET.get('page', 1)

    users_page, total_students, debtors_count, total_debt = await get_users_data(
        request.user, role, filter_type, search, page
    )

    context = {
        'users': users_page,
        'total_students': total_students,
        'debtors_count': debtors_count,
        'total_debt': total_debt,
        'current_role': role,
        'current_filter': filter_type,
        'current_search': search,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'users/user_list.html', context)


@login_required
@permission_required('users', 'create')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Tashkilotni biriktirish
            if not user.organization and request.user.organization:
                user.organization = request.user.organization

            user.save()
            messages.success(request, f"{user.first_name} muvaffaqiyatli qo'shildi!")
            return redirect('users:user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': "Yangi foydalanuvchi"})


# ============================================
# O'QUVCHI QO'SHISH (Majburiy Ota-Ona bilan)
# ============================================
@login_required
@permission_required('users', 'create')
@transaction.atomic
def student_create(request):
    """O'quvchi qo'shish - ota-ona ma'lumotlari majburiy"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. O'quvchini saqlash
            student = form.save(commit=False, organization=request.user.organization)
            student.save()
            
            # 2. Ota-onani yaratish yoki topish
            parent_phone = form.cleaned_data['parent_phone']
            parent_first_name = form.cleaned_data['parent_first_name']
            parent_last_name = form.cleaned_data['parent_last_name']
            relation_type = form.cleaned_data['relation_type']
            
            # Telefon bilan ota-onani qidirish
            parent, created = User.objects.get_or_create(
                phone=parent_phone,
                defaults={
                    'first_name': parent_first_name,
                    'last_name': parent_last_name,
                    'role': 'parent',
                    'organization': request.user.organization,
                    'is_active': True,
                }
            )
            
            # Agar yangi yaratilgan bo'lsa, parol berish
            if created:
                parent.set_password(parent_phone[-4:])  # Telefon oxirgi 4 raqami parol
                parent.save()
            
            # 3. Bog'liqlik yaratish
            ParentStudent.objects.get_or_create(
                parent=parent,
                student=student,
                defaults={
                    'relation_type': relation_type,
                    'is_main_contact': True,
                    'organization': request.user.organization,
                }
            )
            
            messages.success(request, f"✅ {student.full_name} muvaffaqiyatli qo'shildi! Ota-ona: {parent.full_name}")
            return redirect('users:user_list')
    else:
        form = StudentForm()
    
    return render(request, 'users/student_form.html', {
        'form': form, 
        'title': "Yangi O'quvchi Qo'shish"
    })


# ============================================
# O'QITUVCHI QO'SHISH (NFC Card bilan)
# ============================================
@login_required
@permission_required('users', 'create')
def teacher_create(request):
    """O'qituvchi qo'shish - NFC karta va to'liq ma'lumotlar"""
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False, organization=request.user.organization)
            teacher.save()
            
            messages.success(request, f"✅ O'qituvchi {teacher.full_name} muvaffaqiyatli qo'shildi!")
            return redirect('users:user_list')
    else:
        form = TeacherForm()
    
    return render(request, 'users/teacher_form.html', {
        'form': form, 
        'title': "Yangi O'qituvchi Qo'shish"
    })


# ============================================
# XODIM QO'SHISH (Rol va Ruxsatlar bilan)
# ============================================
@login_required
@permission_required('users', 'create')
def staff_create(request):
    """Xodim qo'shish - ruxsatlar bilan"""


    # Bo'limlar va amallar
    from apps.users.forms import AVAILABLE_MODULES, AVAILABLE_ACTIONS

    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            # Ruxsatlarni yig'ish
            permissions = {}
            for module_code, module_name, icon in AVAILABLE_MODULES:
                module_perms = {}
                for action_code, action_name in AVAILABLE_ACTIONS:
                    field_name = f"perm_{module_code}_{action_code}"
                    module_perms[action_code] = field_name in request.POST
                permissions[module_code] = module_perms

            staff = form.save(
                commit=False,
                organization=request.user.organization,
                permissions=permissions
            )
            staff.save()
            
            messages.success(request, f"✅ Xodim {staff.full_name} muvaffaqiyatli qo'shildi!")
            return redirect('users:user_list')
    else:
        form = StaffForm()
    
    return render(request, 'users/staff_form.html', {
        'form': form, 
        'title': "Yangi Xodim Qo'shish",
        'modules': AVAILABLE_MODULES,
        'actions': AVAILABLE_ACTIONS,
    })


@login_required
@permission_required('users', 'edit')
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar yangilandi.")
            return redirect('users:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': "Tahrirlash"})


@login_required
@permission_required('users', 'delete')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.warning(request, "Foydalanuvchi o'chirildi.")
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

