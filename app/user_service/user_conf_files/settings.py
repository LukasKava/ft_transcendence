# settings.py
from pathlib import Path
import os
import environ
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret key (keep it secret in production)
SECRET_KEY = os.getenv('SECRET_KEY3', 'django-insecure-#&!@')  # Default value for development

# Debug mode (set to True for development)
DEBUG = True

# Allow all hosts (use specific hosts for production)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
	'corsheaders',
	'user_conf_files',
	'users',

]

# Middleware configuration
MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ORS_ALLOWED_ORIGINS = [
    'http://localhost:5000',
    'https://localhost:5000',
]

SERVICE_ROUTES = {
    '/ws': 'http://notify_service:3000',
    '/game': 'http://game_service:5000',
}

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
#    'DEFAULT_PERMISSION_CLASSES': (
#        #'rest_framework.permissions.AllowAny',  #This is for development
#        'rest_framework.permissions.IsAuthenticated',  # Require authentication for all views by default
#    ),
}

# Simple JWT settings (optional but recommended)
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), # This is for development
    #'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), #After development this line should be valid 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# URL configuration
ROOT_URLCONF = 'user_conf_files.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'user_conf_files.wsgi.application'


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

AUTH_USER_MODEL = 'users.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}
