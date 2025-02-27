
"""settin
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

import os
import environ

from datetime import timedelta

env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# For https connection 
BASE_URL_SCHEME = 'https'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECRET_KEY = os.environ['SECRET_KEY', 'hZBVwFTiEsVWavJqGiP2VCIdVUtfLjfLTCvbmYimmH3WxpIiaSZyaBJyIbIBVHUz4nM']
HOST_IP = env('HOST_IP')
FRONTEND_URL = env('FRONTEND_URL')

# DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1", FRONTEND_URL]

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
#SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security (HSTS)
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


#KEY_PATH = os.path.join(BASE_DIR, 'certs/privkey.key')
#CERT_PATH = os.path.join(BASE_DIR, 'certs/fullchain.crt')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',# WebSockets and more for Django
	'django.contrib.admin',
    'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',# Toolkit for building Web APIs
    #'django_extensions',
    'djoser',# JWT authentication for DRF
	'rest_framework_simplejwt.token_blacklist', # Blacklist JWT tokens
    'corsheaders',# Handle CORS headers
    'notifications',
	'game',
	'users',
	'friends',
]

ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
     #'default': {
     #    'BACKEND': 'channels_redis.core.RedisChannelLayer',
     #    'CONFIG': {
     #        "hosts": [('127.0.0.1',6379)]
     #    },
     #},
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # for dev
    }
}

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





REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # This is for development
        # 'rest_framework.permissions.IsAuthenticated',  # by default
    ),
}



ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': env('POSTGRES_DB'),
		'USER': env('POSTGRES_USER'),
		'PASSWORD': env('POSTGRES_PASSWORD'),
		'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
	}
}




# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

## Additional locations of static files
#STATICFILES_DIRS = [
#        os.path.join(BASE_DIR, 'staticfiles'),
#        ]
#
# Enable gzip compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# ----------------- OAUTH 2.0 - 42 INTRA SETTINGS -----------------:
# 42 Intra auth URL
API_42_AUTH_URL = 'https://api.intra.42.fr/oauth/authorize'
# 42 Intra access token endpoint
API_42_ACCESS_TOKEN_ENDPOINT = 'https://api.intra.42.fr/oauth/token'
# 42 Intra redirect URI
API_42_REDIRECT_URI = f'{FRONTEND_URL}/42-callback/'
API_42_REDIRECT_URI_MATCH = f'{FRONTEND_URL}/42-callback-match/'
# 42 Intra entrypoint URL
API_42_INTRA_ENTRYPOINT_URL = 'https://api.intra.42.fr/v2/me'
# 42 Intra frontend callback URL
API_42_FRONTEND_CALLBACK_URL = f'${FRONTEND_URL}/auth-success'
# one-time code lifetime in seconds
EXCHANGE_CODE_TIMEOUT = 30
# API CLIENT ID
INTRA_UID_42 = os.environ['CLIENT_ID']
# API CLIENT SECRET
INTRA_SECRET_42 = os.environ['CLIENT_SECRET']

