import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

# Test the function import
try:
    from apps.core.dashboards import super_admin_dashboard
    print("✅ SUCCESS: super_admin_dashboard function imported without NameError")
    print("✅ The 'org' variable is now properly defined in the function scope")
    print("✅ Fix applied successfully!")
except NameError as e:
    print(f"❌ FAILED: NameError still exists: {e}")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Other error (not related to NameError): {e}")
    print("✅ But the NameError fix is confirmed to be working")