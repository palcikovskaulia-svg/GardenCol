from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Завантаження змінних оточення з .env (для локальної розробки)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# 1. СЕКЦІЇ БЕЗПЕКИ ТА DEBUG
# ==========================================================

# Використовуйте змінну середовища для SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev')

# DEBUG тепер контролюється змінною середовища
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Дозволяємо доступ з хостів Render та локально
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'store',
    # WhiteNoise для швидкої обробки статичних файлів
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise повинен бути на самому верху для обробки статичних файлів
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GardenCol_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'GardenCol_Project.wsgi.application'


# ==========================================================
# 2. КОНФІГУРАЦІЯ БАЗИ ДАНИХ (ЛОКАЛЬНО vs RENDER)
# ==========================================================

# Перевіряємо, чи існує змінна DATABASE_URL (існує на Render)
if os.environ.get('DATABASE_URL'):
    # Якщо змінна існує (Production), використовуємо PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Якщо змінна НЕ існує (Локально), використовуємо SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ... (Password validation, Internationalization, Time Zone залишаються без змін) ...

# ==========================================================
# 3. СТАТИЧНІ ТА МЕДІА ФАЙЛИ (WHITENOISE & CLOUDINARY)
# ==========================================================

# Налаштування статичних файлів (CSS/JS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Налаштування WhiteNoise для стиснення та кешування
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Cloudinary: Налаштування для медіа файлів (зображень)
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

# Вказуємо Django використовувати Cloudinary для зберігання медіа-файлів (завантажених користувачем)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'