from main.settings.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'large_csv_prod',
        'USER': 'user_name_here',
        'PASSWORD': 'pwd_here',
        'AUTH_SOURCE': 'large_csv_prod',
        'HOST': 'localhost',
        'PORT': 27017,
    }
}

STATIC_ROOT = 'static/'
