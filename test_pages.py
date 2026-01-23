"""
Barcha sahifalarni avtomatik test qilish.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test sahifalar ro'yxati
PAGES = {
    'Dashboard': '/',
    'Users List': '/users/',
    'Teachers': '/users/teachers/',
    'Students': '/crm/students/',

    # Education
    'Courses': '/courses/',
    'Groups': '/groups/',
    'Rooms': '/rooms/',
    'Materials': '/edu/materials/',

    # Operations
    'Lessons': '/operations/lessons/',
    'Schedule': '/operations/schedule/',
    'Teacher Ratings': '/operations/ratings/teachers/',
    'Student Ratings': '/operations/ratings/students/',

    # Finance
    'Accounts': '/finance/accounts/',
    'Categories': '/finance/categories/',
    'Transactions': '/finance/transactions/',
    'Payroll': '/finance/payroll/',
    'Reports': '/finance/reports/',

    # CRM
    'Pipeline': '/crm/pipeline/',
    'Stages': '/crm/stages/',
    'Sources': '/crm/sources/',

    # Core
    'Settings': '/core/settings/',
    'History': '/core/history/',
}

def test_pages():
    """Barcha sahifalarni test qilish"""
    print("=" * 70)
    print(f"🧪 SAHIFALARNI TEST QILISH - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    results = {
        'success': [],
        'error': [],
        'redirect': []
    }

    session = requests.Session()

    for name, url in PAGES.items():
        full_url = BASE_URL + url
        try:
            response = session.get(full_url, allow_redirects=False, timeout=10)

            if response.status_code == 200:
                results['success'].append((name, url, response.status_code))
                print(f"✅ {name:<25} {url:<40} [{response.status_code}]")
            elif response.status_code in [301, 302, 303, 307, 308]:
                redirect_to = response.headers.get('Location', 'unknown')
                results['redirect'].append((name, url, response.status_code, redirect_to))
                print(f"➡️  {name:<25} {url:<40} [{response.status_code}] -> {redirect_to}")
            else:
                results['error'].append((name, url, response.status_code))
                print(f"❌ {name:<25} {url:<40} [{response.status_code}]")
        except requests.exceptions.RequestException as e:
            results['error'].append((name, url, str(e)))
            print(f"⚠️  {name:<25} {url:<40} [ERROR: {str(e)[:30]}]")

    # Natijalar
    print("\n" + "=" * 70)
    print("📊 NATIJALAR:")
    print("=" * 70)
    print(f"✅ Muvaffaqiyatli: {len(results['success'])}")
    print(f"➡️  Redirect: {len(results['redirect'])}")
    print(f"❌ Xatolik: {len(results['error'])}")
    print()

    if results['error']:
        print("❌ XATOLIKLAR:")
        for item in results['error']:
            if len(item) == 3:
                name, url, status = item
                print(f"   • {name}: {url} [{status}]")
            else:
                name, url, error = item
                print(f"   • {name}: {url} [ERROR: {error}]")

    print("\n" + "=" * 70)

    # JSON formatda saqlash
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(PAGES),
            'success': len(results['success']),
            'redirect': len(results['redirect']),
            'error': len(results['error']),
            'details': results
        }, f, indent=2, ensure_ascii=False)

    print("💾 Natijalar 'test_results.json' ga saqlandi")


if __name__ == '__main__':
    test_pages()
