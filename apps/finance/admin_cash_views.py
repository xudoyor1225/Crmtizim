"""
Administrator kassa kirim-chiqim va kassa topshirish viewlari.
Admin o'z kassasida kirim-chiqim qiladi, keyin super adminga topshiradi.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from .models import Account, Transaction, TransactionCategory, CashSubmission
from apps.users.models import User
from apps.core.permissions import permission_required, check_permission
from apps.core.audit import log_user_action


def _get_or_create_admin_account(user, org):
    """Admin uchun shaxsiy kassani olish yoki yaratish."""
    account = Account.objects.filter(
        organization=org,
        name=f"Admin Kassa - {user.get_full_name()}",
        is_deleted=False,
    ).first()
    if not account:
        account = Account.objects.create(
            organization=org,
            name=f"Admin Kassa - {user.get_full_name()}",
            account_type='cash',
            balance=Decimal('0.00'),
        )
    return account


@login_required
@permission_required('admin_finance', 'view')
def admin_cash_dashboard(request):
    """Administrator kassasi - kirim chiqim dashboard."""
    org = request.organization
    user = request.user
    admin_account = _get_or_create_admin_account(user, org)

    # Admin tranzaksiyalari
    transactions = Transaction.objects.filter(
        account=admin_account,
        is_deleted=False,
        created_by=user,
    ).select_related('category', 'created_by', 'confirmed_by').order_by('-created_at')[:50]

    # Statistika
    confirmed_txs = Transaction.objects.filter(
        account=admin_account,
        is_deleted=False,
        status='confirmed',
    )
    total_income = confirmed_txs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or 0
    total_expense = confirmed_txs.filter(transaction_type='expense').aggregate(t=Sum('amount'))['t'] or 0

    # Oxirgi topshirishlar
    submissions = CashSubmission.objects.filter(
        admin_user=user,
        is_deleted=False,
    ).order_by('-created_at')[:10]

    context = {
        'admin_account': admin_account,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': admin_account.balance,
        'submissions': submissions,
    }
    return render(request, 'finance/admin_cash/dashboard.html', context)


@login_required
@permission_required('admin_finance', 'create')
def admin_add_income(request):
    """Admin kassasiga kirim qo'shish."""
    from .forms import AdminCashTransactionForm
    org = request.organization
    user = request.user
    admin_account = _get_or_create_admin_account(user, org)

    if request.method == 'POST':
        form = AdminCashTransactionForm(request.POST, organization=org, transaction_type='income')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.account = admin_account
            t.transaction_type = 'income'
            t.created_by = user
            t.status = 'pending'
            t.save()
            log_user_action(user, 'CREATE', 'Transaction', t.id, str(t), request=request)
            messages.success(request, "Kirim qo'shildi, tasdiqlash kutilmoqda.")
            return redirect('finance:admin_cash_dashboard')
    else:
        form = AdminCashTransactionForm(organization=org, transaction_type='income')

    return render(request, 'finance/admin_cash/transaction_form.html', {
        'form': form, 'title': 'Kirim', 'type': 'income'
    })


@login_required
@permission_required('admin_finance', 'create')
def admin_add_expense(request):
    """Admin kassasidan chiqim qo'shish."""
    from .forms import AdminCashTransactionForm
    org = request.organization
    user = request.user
    admin_account = _get_or_create_admin_account(user, org)

    if request.method == 'POST':
        form = AdminCashTransactionForm(request.POST, organization=org, transaction_type='expense')
        if form.is_valid():
            t = form.save(commit=False)
            t.organization = org
            t.account = admin_account
            t.transaction_type = 'expense'
            t.created_by = user
            t.status = 'pending'
            t.save()
            log_user_action(user, 'CREATE', 'Transaction', t.id, str(t), request=request)
            messages.success(request, "Chiqim qo'shildi, tasdiqlash kutilmoqda.")
            return redirect('finance:admin_cash_dashboard')
    else:
        form = AdminCashTransactionForm(organization=org, transaction_type='expense')

    return render(request, 'finance/admin_cash/transaction_form.html', {
        'form': form, 'title': 'Chiqim', 'type': 'expense'
    })


@login_required
@permission_required('admin_finance', 'view')
def admin_cash_history(request):
    """Admin kassasi tarixi."""
    org = request.organization
    user = request.user
    admin_account = _get_or_create_admin_account(user, org)

    # Filters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    trans_type = request.GET.get('type', '')

    transactions = Transaction.objects.filter(
        account=admin_account,
        is_deleted=False,
    ).select_related('category', 'created_by', 'confirmed_by')

    if date_from:
        transactions = transactions.filter(created_at__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(created_at__date__lte=date_to)
    if trans_type:
        transactions = transactions.filter(transaction_type=trans_type)

    transactions = transactions.order_by('-created_at')[:100]

    context = {
        'transactions': transactions,
        'admin_account': admin_account,
        'date_from': date_from,
        'date_to': date_to,
        'trans_type': trans_type,
    }
    return render(request, 'finance/admin_cash/history.html', context)


@login_required
@permission_required('admin_finance', 'create')
def admin_submit_cash(request):
    """Admin kassasini asosiy kassaga topshirish."""
    org = request.organization
    user = request.user
    admin_account = _get_or_create_admin_account(user, org)

    # Asosiy kassani topish (admin kassasi bo'lmagan birinchi kassa)
    main_accounts = Account.objects.filter(
        organization=org,
        is_deleted=False,
    ).exclude(pk=admin_account.pk)

    if request.method == 'POST':
        period_type = request.POST.get('period_type', 'weekly')
        main_account_id = request.POST.get('main_account')
        notes = request.POST.get('notes', '')

        main_account = get_object_or_404(Account, pk=main_account_id, organization=org)

        # Davr hisoblash
        today = timezone.now().date()
        if period_type == 'weekly':
            period_start = today - timedelta(days=7)
        else:
            period_start = today - timedelta(days=30)
        period_end = today

        # Davr ichidagi tranzaksiyalar
        period_txs = Transaction.objects.filter(
            account=admin_account,
            is_deleted=False,
            status='confirmed',
            created_at__date__gte=period_start,
            created_at__date__lte=period_end,
        )

        total_income = period_txs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        total_expense = period_txs.filter(transaction_type='expense').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        net_amount = total_income - total_expense

        submission = CashSubmission.objects.create(
            organization=org,
            admin_user=user,
            admin_account=admin_account,
            main_account=main_account,
            total_income=total_income,
            total_expense=total_expense,
            net_amount=net_amount,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            notes=notes,
            status='pending',
        )

        log_user_action(user, 'CREATE', 'CashSubmission', submission.id, str(submission), request=request)
        messages.success(request, f"Kassa topshirish so'rovi yuborildi. Sof summa: {net_amount:,.0f} UZS")
        return redirect('finance:admin_cash_dashboard')

    context = {
        'admin_account': admin_account,
        'main_accounts': main_accounts,
        'balance': admin_account.balance,
    }
    return render(request, 'finance/admin_cash/submit_cash.html', context)


# ============================================
# SUPER ADMIN / OWNER - Kassa topshirishlarni boshqarish
# ============================================

@login_required
@permission_required('finance', 'view')
def cash_submission_list(request):
    """Kassa topshirishlar ro'yxati (super admin / owner)."""
    org = request.organization
    status_filter = request.GET.get('status', '')

    submissions = CashSubmission.objects.filter(is_deleted=False)
    if org:
        submissions = submissions.filter(organization=org)
    if status_filter:
        submissions = submissions.filter(status=status_filter)

    submissions = submissions.select_related(
        'admin_user', 'admin_account', 'main_account', 'approved_by'
    ).order_by('-created_at')[:50]

    context = {
        'submissions': submissions,
        'status_filter': status_filter,
    }
    return render(request, 'finance/admin_cash/submission_list.html', context)


@login_required
@permission_required('finance', 'edit')
@require_POST
def approve_cash_submission(request, pk):
    """Kassa topshirishni tasdiqlash - pul asosiy kassaga o'tadi."""
    from .services import approve_cash_submission as approve_service
    try:
        approve_service(pk, request.user)
        messages.success(request, "Kassa topshirish tasdiqlandi. Pul asosiy kassaga o'tkazildi.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('finance:cash_submission_list')


@login_required
@permission_required('finance', 'edit')
@require_POST
def reject_cash_submission(request, pk):
    """Kassa topshirishni rad etish."""
    submission = get_object_or_404(CashSubmission, pk=pk)
    if submission.status != 'pending':
        messages.error(request, "Bu topshirish allaqachon ko'rib chiqilgan.")
        return redirect('finance:cash_submission_list')

    rejection_reason = request.POST.get('reason', '')
    submission.status = 'rejected'
    submission.rejection_reason = rejection_reason
    submission.approved_by = request.user
    submission.approved_at = timezone.now()
    submission.save()

    log_user_action(request.user, 'UPDATE', 'CashSubmission', submission.id,
                    f"Rad etildi: {submission}", request=request)
    messages.warning(request, "Kassa topshirish rad etildi.")
    return redirect('finance:cash_submission_list')
