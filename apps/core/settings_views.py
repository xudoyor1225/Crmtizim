"""
Settings (Sozlamalar) sahifalari.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.finance.models import TransactionCategory, Account
from apps.users.models import User
from apps.organizations.models import Organization


@login_required
def settings_index(request):
    """Asosiy sozlamalar sahifasi"""
    org = request.user.organization
    user = request.user

    # Statistika
    stats = {
        'categories_count': TransactionCategory.objects.filter(organization=org).count() if org else 0,
        'accounts_count': Account.objects.filter(organization=org, is_deleted=False).count() if org else 0,
        'users_count': User.objects.filter(organization=org, is_deleted=False).count() if org else 0,
    }

    context = {
        'stats': stats,
    }

    return render(request, 'core/settings.html', context)
