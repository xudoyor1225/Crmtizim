import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

def check_cash_submission_table():
    """Check if the finance_cash_submissions table has the required columns"""
    cursor = connection.cursor()
    
    # Check table structure
    if connection.vendor == 'sqlite':
        cursor.execute("PRAGMA table_info(finance_cash_submissions)")
        columns = cursor.fetchall()
        print("SQLite table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    elif connection.vendor == 'postgresql':
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'finance_cash_submissions'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        print("PostgreSQL table columns:")
        for col in columns:
            print(f"  {col[0]} ({col[1]})")
    
    # Check for required columns
    required_columns = ['amount_cash', 'amount_card', 'amount_terminal', 'amount_other']
    existing_columns = [col[1] if connection.vendor == 'sqlite' else col[0] for col in columns]
    
    missing_columns = [col for col in required_columns if col not in existing_columns]
    
    if missing_columns:
        print(f"\n❌ Missing columns: {missing_columns}")
        print("Migration 0008 needs to be applied!")
        return False
    else:
        print("\n✅ All required columns are present")
        return True

if __name__ == "__main__":
    check_cash_submission_table()