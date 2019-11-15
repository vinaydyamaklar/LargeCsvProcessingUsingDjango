"""
Django settings for main(WoofyaAPIDashboard) project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&w)na9%0on(_+#$1#h@52ndc=+$&k3hp01pv^7=%f_ru%$$r2k'

ALLOWED_HOSTS = ['*']

# AUTH_USER_MODEL = '' TODO: update it with the User account model

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user_account',
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

ROOT_URLCONF = 'main.urls'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH, ],
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

WSGI_APPLICATION = 'main.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = ['%I:%M %p']

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # your size limit in bytes

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_PATH = os.path.join(BASE_DIR, 'site_static')  # Absolute path to the static directory
STATICFILES_DIRS = (
    STATIC_PATH,
)

DOMAIN_URL = 'http://127.0.0.1:8000/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'sessionid',
)
CORS_EXPOSE_HEADERS = (
    'set-cookie',
    'sessionid',
)

# Accepted input types
VALID_IMAGE_FILE_TYPES = ['JPEG', 'PNG', 'JPG']

###########################
# ENVIRONMENT DETAILS
###########################
PROD = 'PROD'
DEVELOPERS = 'DEVELOPERS'
DEPLOYMENT_ENVS = [PROD, DEVELOPERS]

ENVIRONMENT = os.environ.get('WOOFY_EMOJIDATA_ENV', DEVELOPERS)

if ENVIRONMENT not in DEPLOYMENT_ENVS:
    print(ENVIRONMENT)
    print('Invalid ENVIRONMENT in config %s' % ENVIRONMENT)
    print('VALID_ENVIRONMENTS ', DEPLOYMENT_ENVS)
    exit(-1)


if ENVIRONMENT == PROD:
    from main.settings.prod import *
elif ENVIRONMENT == DEVELOPERS:
    from main.settings.local import *

