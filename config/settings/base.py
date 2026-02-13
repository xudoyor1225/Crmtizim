import os
from pathlib import Path
from decouple import config, Csv

# 1. PATHS
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 2. SECURITY
# .env faylidan o'qiladi
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-only-for-local-testing-change-this')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='13.39.83.160,localhost,127.0.0.1', cast=Csv())

# 3. APPS
INSTALLED_APPS = [
    # Unfold admin (django.contrib.admin dan oldin bo'lishi kerak)
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    'rest_framework',
    'corsheaders',
    'apps.api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # UCHINCHI TOMON KUTUBXONALARI
    'widget_tweaks',  # pip install django-widget-tweaks

    # BIZNING APPLAR (To'liq yo'l bilan)
    'apps.core',
    'apps.organizations',
    'apps.users',
    'apps.education',
    'apps.crm',
    'apps.finance',
    'apps.operations',
    'apps.automation',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # BIZNING MIDDLEWARE
    'apps.core.middleware.TenantMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.tenant_context',
                'apps.core.context_processors.user_permissions_context',
                'apps.core.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 4. DATABASE
# PostgreSQL yoki SQLite tanlash
USE_POSTGRES = config('USE_POSTGRES', default=False, cast=bool)

if USE_POSTGRES:
    # PostgreSQL sozlamalari
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='crmtizim_db'),
            'USER': config('DB_USER', default='crmtizim_user'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'client_encoding': 'UTF8',
            },
        }
    }
else:
    # SQLite sozlamalari (development uchun)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 5. AUTH
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# 6. I18N
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# 7. STATIC & MEDIA
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 8. AUTOMATION
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# --- YANGI SOZLAMALAR (Script orqali) ---

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# CELERY & REDIS (Temporarily disabled - install celery first)
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TIMEZONE = 'Asia/Tashkent'

# CORS (Mobil ilova uchun)
# ⚠️ Production'da faqat o'z domenlaringizni ruxsat bering!
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # Faqat development uchun
else:
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'https://app.smartedu.uz,https://admin.smartedu.uz'
    ).split(',')


# OPTIMIZATION: WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import mimetypes
mimetypes.add_type('application/javascript', '.js', True)

# STATIC FIX
if DEBUG:
    import os
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Logs papkasini yaratish
import os
LOGS_DIR = BASE_DIR / 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


# ========================================
# UNFOLD ADMIN PANEL SOZLAMALARI
# ========================================
from django.templatetags.static import static
from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "Smart EDU CRM",
    "SITE_HEADER": "Smart EDU CRM",
    "SITE_SYMBOL": "school",  # Material Symbols icon nomi
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "apps.core.admin.environment_callback",
    "DASHBOARD_CALLBACK": "apps.core.admin.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "240 253 250",
            "100": "204 251 241",
            "200": "153 246 228",
            "300": "94 234 212",
            "400": "45 212 191",
            "500": "29 84 109",  # #1D546D - main brand color
            "600": "13 79 102",
            "700": "15 75 99",
            "800": "17 63 84",
            "900": "6 30 41",
            "950": "4 21 29",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Boshqaruv",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("dashboard"),
                    },
                    {
                        "title": "Foydalanuvchilar",
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                ],
            },
            {
                "title": "Ta'lim",
                "separator": True,
                "items": [
                    {
                        "title": "Guruhlar",
                        "icon": "groups",
                        "link": reverse_lazy("admin:education_group_changelist"),
                    },
                    {
                        "title": "Kurslar",
                        "icon": "book",
                        "link": reverse_lazy("admin:education_course_changelist"),
                    },
                    {
                        "title": "Xonalar",
                        "icon": "meeting_room",
                        "link": reverse_lazy("admin:education_room_changelist"),
                    },
                ],
            },
            {
                "title": "Moliya",
                "separator": True,
                "items": [
                    {
                        "title": "Tranzaksiyalar",
                        "icon": "payments",
                        "link": reverse_lazy("admin:finance_transaction_changelist"),
                    },
                    {
                        "title": "Hisoblar",
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:finance_account_changelist"),
                    },
                ],
            },
            {
                "title": "CRM",
                "separator": True,
                "items": [
                    {
                        "title": "Lidlar",
                        "icon": "funnel",
                        "link": reverse_lazy("admin:crm_lead_changelist"),
                    },
                    {
                        "title": "Bosqichlar",
                        "icon": "view_kanban",
                        "link": reverse_lazy("admin:crm_stage_changelist"),
                    },
                ],
            },
            {
                "title": "Tashkilot",
                "separator": True,
                "items": [
                    {
                        "title": "Tashkilotlar",
                        "icon": "business",
                        "link": reverse_lazy("admin:organizations_organization_changelist"),
                    },
                    {
                        "title": "Filiallar",
                        "icon": "store",
                        "link": reverse_lazy("admin:organizations_branch_changelist"),
                    },
                ],
            },
        ],
    },
}

