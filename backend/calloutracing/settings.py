"""
Django settings for calloutracing project.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Parse ALLOWED_HOSTS from environment variable, stripping whitespace
ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',') if host.strip()]  # type: ignore

# Add Railway domain to allowed hosts
if 'RAILWAY_STATIC_URL' in os.environ:
    try:
        railway_domain = os.environ['RAILWAY_STATIC_URL'].replace('https://', '').replace('http://', '')
        # Only add if it's not a backend domain and not already in the list
        if railway_domain and not railway_domain.endswith('-backend.up.railway.app') and railway_domain not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(railway_domain)
    except Exception:
        pass  # Silently fail if there's an issue with the domain

# Add common Railway domains
ALLOWED_HOSTS.extend([
    'calloutracing.up.railway.app',
    '.railway.app',
    '.up.railway.app'
])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    
    # Local apps
    'core',
    'api',
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
]

ROOT_URLCONF = 'calloutracing.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'calloutracing.wsgi.application'

# Database
# Use PostgreSQL by default, fallback to SQLite if not configured
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
elif 'Postgres.DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ['Postgres.DATABASE_URL'])
    }
else:
    # Default to Railway PostgreSQL for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='railway'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK'),
            'HOST': config('DB_HOST', default='caboose.proxy.rlwy.net'),
            'PORT': config('DB_PORT', default='33954'),
        }
    }

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Only add static files dirs if the directory exists
STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use custom User model
AUTH_USER_MODEL = 'core.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://calloutracing.up.railway.app',
    'https://calloutracing-backend-production.up.railway.app',
    'https://calloutracing-backend.up.railway.app',
]

# Add any additional origins from environment variable
try:
    env_origins_str = config('CORS_ALLOWED_ORIGINS', default='')
    if isinstance(env_origins_str, str) and env_origins_str:
        env_origins = env_origins_str.split(',')
        for origin in env_origins:
            origin = origin.strip()
            if origin and origin not in CORS_ALLOWED_ORIGINS:
                CORS_ALLOWED_ORIGINS.append(origin)
except Exception:
    pass

# Add Railway frontend domain to CORS if available
if 'RAILWAY_STATIC_URL' in os.environ:
    try:
        railway_frontend = os.environ['RAILWAY_STATIC_URL']
        # Only add if it's a valid URL with scheme and not a backend domain
        if (railway_frontend and 
            railway_frontend.startswith(('http://', 'https://')) and
            not railway_frontend.endswith('-backend.up.railway.app') and
            railway_frontend not in CORS_ALLOWED_ORIGINS):
            CORS_ALLOWED_ORIGINS.append(railway_frontend)
    except Exception:
        pass

# Debug: Print CORS origins in development
if DEBUG:
    print(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Additional CORS settings for better compatibility
CORS_EXPOSE_HEADERS = [
    'content-type',
    'content-disposition',
]
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    # Disable SSL redirect for now to avoid 301 redirects
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@calloutracing.com')

# Frontend URL for email verification links
FRONTEND_URL = config('FRONTEND_URL', default='https://calloutracing.up.railway.app')

# Additional Gmail settings for App Passwords
if EMAIL_HOST == 'smtp.gmail.com':
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

# Add these at the end of the file for cross-site session support
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

# Stripe Configuration
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')

# Frontend URL for Stripe redirects
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')

# Marketplace commission percentage
MARKETPLACE_COMMISSION_PERCENTAGE = config('MARKETPLACE_COMMISSION_PERCENTAGE', default=0.05, cast=float)  # 5% default 