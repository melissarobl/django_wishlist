"""
Django settings for wishlist project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from google.oauth2 import service_account


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)%f3z85p=)&9^1!3t5(xzf$vte80wfx34(4yag)m0&pv8ems+v'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('GAE_INSTANCE'):
    DEBUG = False
else:
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
    'travel_wishlist'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wishlist.urls'

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

WSGI_APPLICATION = 'wishlist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Default settings - will work at App Engine GCP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'places',
        'USER': 'traveler',
        'PASSWORD': os.getenv('TRAVELER_PW'),
        'HOST': '/cloudsql/wishlist-django-442619:us-central1:wishlist-db-mysql',
        'PORT': '3306'
    }
}

# connect to the same db when this code is running on our computer
# here, we need to connect via the cloud proxy
# test if we are running locally and modify db settings for local development

if not os.getenv('GAE_INSTANCE'):
    # app is not running at GAE, use local settings
    # DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# Specify location to copy static files to when running python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

# Where in the file system to save user-uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


if not os.getenv('GAE_INSTANCE'):  # not running at GCP -local development
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
else: # else, running at GCP
    GS_STATIC_FILE_BUCKET = 'wishlist-django-442619.appspot.com'
    STATIC_URL = f'https://storage.cloud.google.com/{GS_STATIC_FILE_BUCKET}/static/'

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'users_wishlist_image_uploads'  # the media bucket name
    MEDIA_URL = f'https://storage.cloud.google.com/{GS_BUCKET_NAME}/media/'

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file('travel_credentials.json')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

#DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
