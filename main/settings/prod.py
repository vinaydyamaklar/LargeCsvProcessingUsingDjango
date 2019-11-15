from main.settings.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': 'lFHPtCeKqCn4GOic',
        'HOST': '35.238.115.230',
        'PORT': '5432',
    }
}

STATIC_ROOT = 'static/'
