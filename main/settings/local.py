from main.settings.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'large_csv',
        'USER': 'csv_user',
        'PASSWORD': 'csv_kjniuyn!kn',
        'AUTH_SOURCE': 'large_csv',
        'HOST': 'localhost',
        'PORT': 27017,
    }
}

STATIC_ROOT = 'static/'
