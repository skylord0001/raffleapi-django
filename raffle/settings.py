from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(#k+1q+y%ln19j7&2b79ba1v=b-b(v^u3w8)g+-i&hxyas85$$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'corsheaders',
    'storages',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ORIGIN_ALLOW_ALL = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'raffle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tmplat')],
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

WSGI_APPLICATION = 'raffle.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


"""
# Import Google libraries
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Configure Google Cloud Storage settings
GS_BUCKET_NAME = 'ltraffle'
GS_PROJECT_ID = 'ltraffle'

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)
credentials_json = 'ltraffle.json'
credentials = service_account.Credentials.from_service_account_file(credentials_json)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
GS_CREDENTIALS = scoped_credentials
"""


MEDIA_URL = '/images/'
MEDIA_DIRS = [
    os.path.join(BASE_DIR, 'zmedias'),
]



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/accounts/profile/'
