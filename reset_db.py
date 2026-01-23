import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent


def clean_project():
    print("🧹 Loyiha tozalanmoqda...")

    # 1. Eski bazani o'chirish
    db_path = BASE_DIR / "db.sqlite3"
    if db_path.exists():
        os.remove(db_path)
        print("✅ db.sqlite3 o'chirildi.")
    else:
        print("ℹ️  db.sqlite3 topilmadi (bu yaxshi).")

    # 2. Migratsiya fayllarini tozalash (faqat __init__.py qoladi)
    apps_dir = BASE_DIR / "apps"
    if apps_dir.exists():
        for app_dir in apps_dir.iterdir():
            migration_dir = app_dir / "migrations"
            if migration_dir.exists() and migration_dir.is_dir():
                for file in migration_dir.iterdir():
                    if file.name != "__init__.py" and file.name != "__pycache__":
                        if file.is_file():
                            os.remove(file)
                        elif file.is_dir():
                            shutil.rmtree(file)
                print(f"✅ {app_dir.name} migratsiyalari tozalandi.")

    print("\n✨ TOZALASH TUGADI! Endi quyidagi buyruqlarni bering:")
    print("1. python manage.py makemigrations core users organizations crm education finance operations automation")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")


if __name__ == "__main__":
    clean_project()