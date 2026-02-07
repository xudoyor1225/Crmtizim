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

