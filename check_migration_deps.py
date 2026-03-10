"""
Migration Dependency Checker
Run this to verify all migration dependencies are correctly set up
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db.migrations.loader import MigrationLoader
from django.db import connection

def check_migrations():
    print("=" * 80)
    print("MIGRATION DEPENDENCY CHECKER")
    print("=" * 80)
    
    loader = MigrationLoader(connection)
    
    # Check for errors
    if loader.graph.has_cycles():
        print("❌ ERROR: Cycle detected in migration graph!")
        return False
    
    # Check finance app migrations
    print("\n📋 Finance App Migrations:")
    finance_migrations = [k for k in loader.disk_migrations.keys() if k[0] == 'finance']
    for app_label, name in sorted(finance_migrations):
        migration = loader.disk_migrations[(app_label, name)]
        print(f"  ✓ {name}")
        print(f"    Dependencies: {migration.dependencies}")
    
    # Check users app migrations
    print("\n📋 Users App Migrations:")
    users_migrations = [k for k in loader.disk_migrations.keys() if k[0] == 'users']
    for app_label, name in sorted(users_migrations):
        migration = loader.disk_migrations[(app_label, name)]
        print(f"  ✓ {name}")
        print(f"    Dependencies: {migration.dependencies}")
    
    # Check specific migration 0010
    print("\n🔍 Checking finance.0010_add_student_to_supply_transaction:")
    try:
        migration_0010 = loader.disk_migrations.get(('finance', '0010_add_student_to_supply_transaction'))
        if migration_0010:
            print(f"  ✓ Migration found")
            print(f"    Dependencies: {migration_0010.dependencies}")
            
            # Verify each dependency exists
            for dep_app, dep_name in migration_0010.dependencies:
                if (dep_app, dep_name) in loader.disk_migrations:
                    print(f"      ✓ {dep_app}.{dep_name} EXISTS")
                else:
                    print(f"      ❌ {dep_app}.{dep_name} NOT FOUND")
                    return False
            
            print("\n✅ All dependencies are valid!")
            return True
        else:
            print("  ❌ Migration not found!")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = check_migrations()
    sys.exit(0 if success else 1)
