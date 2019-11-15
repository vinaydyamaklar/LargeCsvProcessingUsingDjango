from main.settings.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'emproto_csv_db',
        'USER': 'csv_user',
        'PASSWORD': 'csv_pwd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = 'static/'
