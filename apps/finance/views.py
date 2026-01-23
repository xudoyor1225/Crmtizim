from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import timedelta
from .models import Account, Transaction, TransactionCategory
from apps.users.models import User
from apps.core.audit import log_user_action

@login_required
def transaction_list(request):
    org = request.organization

    # Filter parametrlari
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    trans_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    account_id = request.GET.get('account', '')

    # Asosiy QuerySet
    transactions = Transaction.objects.filter(is_deleted=False)
    if org:
        transactions = transactions.filter(organization=org)

    if date_from:
        transactions = transactions.filter(created_at__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(created_at__date__lte=date_to)
    if trans_type:
        transactions = transactions.filter(transaction_type=trans_type)
    if status:
        transactions = transactions.filter(status=status)
    if account_id:
        transactions = transactions.filter(account_id=account_id)

    # Statistika (Safe Aggregation)
    # Filterlangan natijalar bo'yicha emas, umumiy org bo'yicha (yoki filter bo'yicha - talabga qarab)
    # Hozircha filterlangan bo'yicha ko'rsatamiz:

    stats_qs = transactions.filter(status='confirmed')
    income = stats_qs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or 0
    expense = stats_qs.filter(transaction_type='expense').aggregate(t=Sum('amount'))['t'] or 0

    # Optimallashtirilgan load
    transactions = transactions.select_related(
        'account', 'category', 'student', 'staff', 'created_by', 'confirmed_by'
    ).order_by('-created_at')[:100]

    accounts = Account.objects.filter(is_deleted=False)
    if org:
        accounts = accounts.filter(organization=org)

    context = {
        'transactions': transactions,
        'accounts': accounts,
        'income': income,
        'expense': expense,
        'balance': income - expense,
        'date_from': date_from,
        'date_to': date_to,
        'trans_type': trans_type,
        'status': status,
        'account_id': account_id,
    }
    return render(request, 'finance/transaction_list.html', context)

# Boshqa viewlar o'zgarishsiz qolishi mumkin, chunki asosiy xato List view da edi
# (Qisqartirish uchun faqat listni yozdim, qolganlari import qilingan joyda turibdi deb faraz qilamiz
# Lekin faylni to'liq yozayotganimiz uchun ularni ham qo'shish kerak)

@login_required
def account_list(request):
    org = request.organization
    accounts = Account.objects.filter(is_deleted=False)
    if org:
        accounts = accounts.filter(organization=org)

    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0

    return render(request, 'finance/account_list.html', {'accounts': accounts, 'total_balance': total_balance})

@login_required
def account_create(request):
    from .forms import AccountForm
    org = request.organization
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.organization = org
            acc.save()
            messages.success(request, "Kassa yaratildi")
            return redirect('finance:account_list')
    else:
        form = AccountForm()
    return render(request, 'finance/account_form.html', {'form': form, 'title': 'Yangi Kassa'})

@login_required
def account_edit(request, pk):
    from .forms import AccountForm
    org = request.organization
    account = get_object_or_404(Account, pk=pk, organization=org)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Kassa yangilandi")
            return redirect('finance:account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'finance/account_form.html', {'form': form, 'title': 'Kassani tahrirlash'})

# ===========================================
# KATEGORIYALAR (Transaction Categories)
# ===========================================

@login_required
def category_list(request):
    """Kirim va chiqim kategoriyalari ro'yxati"""
    org = request.organization
    categories = TransactionCategory.objects.filter(is_deleted=False)
    if org:
        categories = categories.filter(organization=org)

    income_categories = categories.filter(transaction_type='income')
    expense_categories = categories.filter(transaction_type='expense')

    return render(request, 'finance/category_list.html', {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
    })

@login_required
def category_create(request):
    """Yangi kategoriya yaratish"""
    from .forms import CategoryForm
    org = request.organization
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.organization = org
            cat.save()
            messages.success(request, "Kategoriya yaratildi")
            return redirect('finance:category_list')
    else:
        form = CategoryForm()
    return render(request, 'finance/category_form.html', {'form': form, 'title': 'Yangi Kategoriya'})

@login_required
def category_edit(request, pk):
    """Kategoriyani tahrirlash"""
    from .forms import CategoryForm
    org = request.organization
    category = get_object_or_404(TransactionCategory, pk=pk, organization=org)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya yangilandi")
            return redirect('finance:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'finance/category_form.html', {'form': form, 'title': 'Kategoriyani tahrirlash'})

@login_required
def add_income(request):
    from .forms import TransactionForm
    org = request.organization
    if request.method == 'POST':
        form = TransactionForm(request.POST, organization=org, transaction_type='income')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.transaction_type = 'income'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "Kirim qo'shildi")
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm(organization=org, transaction_type='income')
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Kirim', 'type': 'income'})

@login_required
def add_expense(request):
    from .forms import TransactionForm
    org = request.organization
    if request.method == 'POST':
        form = TransactionForm(request.POST, organization=org, transaction_type='expense')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.transaction_type = 'expense'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "Chiqim qo'shildi")
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm(organization=org, transaction_type='expense')
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Chiqim', 'type': 'expense'})

@login_required
def confirm_transaction(request, pk):
    # Bu view endi services.py orqali ishlaydi (avvalgi fixda to'g'irlangan)
    from .services import confirm_transaction as confirm_service
    try:
        confirm_service(pk, request.user)
        messages.success(request, "Tasdiqlandi")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('finance:transaction_list')

@login_required
def reject_transaction(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    if t.status == 'pending':
        t.status = 'rejected'
        t.save()
        messages.warning(request, "Rad etildi")
    return redirect('finance:transaction_list')

# Student payments view (Placeholder - needs existing imports)
@login_required
def student_payments(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    payments = Transaction.objects.filter(student=student).order_by('-created_at')
    total = payments.filter(transaction_type='income', status='confirmed').aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'finance/student_payments.html', {'student': student, 'payments': payments, 'total_paid': total})

@login_required
def add_student_payment(request, student_id):
    from .forms import StudentPaymentForm
    student = get_object_or_404(User, pk=student_id)
    if request.method == 'POST':
        form = StudentPaymentForm(request.POST, request.FILES, organization=request.organization)
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = request.organization
            t.student = student
            t.transaction_type = 'income'
            t.created_by = request.user
            t.status = 'pending'
            t.save()
            messages.success(request, "To'lov qabul qilindi")
            return redirect('finance:student_payments', student_id=student.id)
    else:
        form = StudentPaymentForm(organization=request.organization)
    return render(request, 'finance/student_payment_form.html', {'form': form, 'student': student})

@login_required
def finance_report(request):
    return render(request, 'finance/report.html', {})

@login_required
def pending_receipts(request):
    txs = Transaction.objects.filter(receipt_verified=False, status='pending')
    return render(request, 'finance/pending_receipts.html', {'pending_receipts': txs})

@login_required
def verify_receipt(request, pk):
    return confirm_transaction(request, pk)

@login_required
def reject_receipt(request, pk):
    return reject_transaction(request, pk)
