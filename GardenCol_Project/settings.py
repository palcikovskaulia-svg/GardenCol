from pathlib import Path
import os # Додано імпорт os для змінних середовища
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# 1. СЕКЦІЇ БЕЗПЕКИ ТА DEBUG (КОНФІГУРАЦІЯ PRODUCTION)
# ==========================================================

# SECURITY WARNING: keep the secret key used in production secret!
# Використовуйте змінну середовища для SECRET_KEY у production
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG тепер контролюється змінною середовища
DEBUG = os.environ.get('DEBUG', 'False') == 'True' 

# ALLOWED_HOSTS: Дозволяємо доступ з хостів Render
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'store',
    # Додаємо WhiteNoise до INSTALLED_APPS для збору статичних файлів
    'whitenoise.runserver_nostatic', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # WhiteNoise повинен бути на самому верху для роботи зі статикою
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- ДОДАНО: Для обробки статичних файлів на Render
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
# 2. КОНФІГУРАЦІЯ БАЗИ ДАНИХ (PostgreSQL)
# ==========================================================

# Database: Використовуємо dj_database_url для підключення до PostgreSQL
# (Render надасть DATABASE_URL через змінну середовища)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600 # Максимальний час життя з'єднання
    )
}

# ... (Password validation, Internationalization, Time Zone залишаються без змін) ...


# ==========================================================
# 3. СТАТИЧНІ ТА МЕДІА ФАЙЛИ (ОБРОБКА WHITENOISE)
# ==========================================================

STATIC_URL = '/static/'
# Створення папки для зібраних статичних файлів у production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Директорії, де Django шукатиме статичні файли (окрім папок static/ у застосунках)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Налаштування WhiteNoise для стиснення та кешування
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA files (зображення, завантажені користувачем)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Папка, де будуть зберігатися файли


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Доданий імпорт os, який був у кінці, тепер перенесено на початок