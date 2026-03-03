#!/usr/bin/env python
"""
Script to create test data for super admin quick payment functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from decimal import Decimal
from apps.users.models import User
from apps.organizations.models import Organization, Branch
from apps.finance.models import Account

def create_test_data():
    print("=" * 50)
    print("CREATING TEST DATA")
    print("=" * 50)

    # Create Organization
    print("\nCreating Organization...")
    org, created = Organization.objects.get_or_create(
        name="Test Organization",
        defaults={
            'subdomain': 'test',
            'is_active': True,
        }
    )
    if created:
        print(f"   ✅ Organization created: {org.name}")
    else:
        print(f"   ℹ️  Organization exists: {org.name}")

    # Create Branch
    print("\nCreating Branch...")
    branch, created = Branch.objects.get_or_create(
        organization=org,
        name="Main Branch",
        defaults={
            'is_main': True,
        }
    )
    if created:
        print(f"   ✅ Branch created: {branch.name}")

    # Create Test Accounts
    print("\nCreating Test Accounts...")
    account_names = ['Main Cash', 'Bank Account', 'Card Terminal']
    accounts_created = 0
    
    for acc_name in account_names:
        account, created = Account.objects.get_or_create(
            organization=org,
            name=acc_name,
            defaults={
                'balance': Decimal('1000000'),
                'account_type': 'cash' if 'Cash' in acc_name else 'bank',
            }
        )
        if created:
            print(f"   ✅ Account created: {account.name}")
            accounts_created += 1
        else:
            print(f"   ℹ️  Account exists: {account.name}")

    # Create Test Student
    print("\nCreating Test Student...")
    student, created = User.objects.get_or_create(
        phone='+998910000001',
        defaults={
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'student',
            'organization': org,
            'branch': branch,
            'is_active': True,
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f"   ✅ Student created: {student.full_name}")
    else:
        print(f"   ℹ️  Student exists: {student.full_name}")

    print("\n" + "=" * 50)
    print("TEST DATA CREATION COMPLETE")
    print("=" * 50)
    print(f"""
📊 SUMMARY:
   • Organization: {org.name}
   • Branch: {branch.name}
   • Accounts: {Account.objects.filter(organization=org, is_deleted=False).count()}
   • Student: {student.full_name} (+998910000001 / student123)
    """)

if __name__ == "__main__":
    create_test_data()