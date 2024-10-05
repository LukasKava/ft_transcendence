# settings.py

from pathlib import Path
import os
import environ
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key (keep it secret in production)
SECRET_KEY = os.getenv('SECRET_KEY3')

# Debug mode (set to True for development)
DEBUG = True

# Allow all hosts (use specific hosts for production)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Installed applications
INSTALLED_APPS = [
	'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
	'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'corsheaders',
	'user_conf_files',
	'user_project',
]

# Middleware configuration
MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',  # Must be at the top
	# 'user_project.middleware.ForceHttpsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

# ORS_ALLOWED_ORIGINS = [
#     'http://localhost:5000',
#     'https://localhost:5000',
# ]

# SERVICE_ROUTES = {
#     '/ws': 'http://notify_service:3000',
#     '/game': 'http://game_service:5000',
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Require authentication for all views by default
    ),
}

# Simple JWT settings (optional but recommended)
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
# }

# URL configuration
ROOT_URLCONF = 'user_project.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'user_conf_files/templates', 
        ],
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

# WSGI application
WSGI_APPLICATION = 'user_project.wsgi.application'
AUTH_USER_MODEL = 'user_conf_files.CustomUser'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# DEFAULT_AVATAR_PATH = os.path.join(MEDIA_ROOT, 'avatars/default_avatar.png')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/register/'
# USE_X_FORWARDED_HOST = True  # Trust the X-Forwarded-Host header
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Trust the X-Forwarded-Proto header
# SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
# SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
# CSRF_COOKIE_SECURE = True  # CSRF cookies should be secure

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_UP_DB'),
        'USER': os.environ.get('DB_UP_USER'),
        'PASSWORD': os.environ.get('DB_UP_PASSWORD'),
        'HOST': os.environ.get('DB_UP_HOST'),
        'PORT': os.environ.get('DB_UP_PORT'),
    }
}


DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Password validators
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

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8081')

CORS_ALLOW_CREDENTIALS = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Directory where static files will be collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
