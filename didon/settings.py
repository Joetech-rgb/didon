# didon/settings.py

from pathlib import Path
# [NEW] Import config and Csv (for ALLOWED_HOSTS)
from decouple import config, Csv
# [NEW] Import dj_database_url for easy database configuration
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# 1. SECURITY WARNING: Keep the secret key used in production secret!
# [CHANGED] Load SECRET_KEY from the environment (.env file)
SECRET_KEY = config('SECRET_KEY')


# 2. SECURITY WARNING: Don't run with debug turned on in production!
# [CHANGED] Load DEBUG from the environment, defaulting to False in production
DEBUG = config('DEBUG', default=False, cast=bool)


# 3. [CHANGED] Load ALLOWED_HOSTS from the environment. Csv casts it to a list.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # [NEW] WhiteNoise must be above staticfiles in production
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    
    'SwiftLogix', 
    # [NEW] Django Crispy Forms for better form rendering (optional but common)
    # 'crispy_forms', 
    # 'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # [NEW] WhiteNoise middleware for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'didon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'didon.wsgi.application'

# 4. Database Configuration (PostgreSQL for Production)
# [CHANGED] Use dj_database_url or manual config to switch to PostgreSQL
# This setup uses config() to load your DB credentials from the .env file

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', 
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}") # Fallback to SQLite if DATABASE_URL is not set
    )
}

# MANUAL POSTGRESQL CONFIG (If you prefer manual entry over DATABASE_URL)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST', 'localhost'),
#         'PORT': config('DB_PORT', '5432'),
#     }
# }


# Password validation... (No change needed here)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization... (No change needed here)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# 5. Static files (Production Serving with WhiteNoise)
# [CHANGED] Enable WhiteNoise compression and caching

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# [NEW] WhiteNoise Settings for efficient static file serving
# This ensures compressed, cached static files are served by the WSGI server
# (This is a common temporary solution before moving to a dedicated CDN/S3)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type... (No change needed here)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication Settings... (No change needed here)
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'


# Email settings (CRITICAL for password reset in production)
# You MUST configure a real email service (SendGrid, Mailgun, etc.) for a live site.
# For now, we will leave it commented out, but this is a required future step.
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')