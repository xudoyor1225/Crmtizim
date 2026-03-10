import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import execute_from_command_line
import sys

def apply_migration():
    """Apply the missing migration for cash submission payment method fields"""
    try:
        # Apply the specific migration
        execute_from_command_line(['manage.py', 'migrate', 'finance', '0008_add_payment_method_fields_to_cash_submission'])
        print("✅ Migration applied successfully!")
        return True
    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        return False

if __name__ == "__main__":
    apply_migration()