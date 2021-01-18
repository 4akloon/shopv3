import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '=)r3242v23_1%4++(%et8j(b)ksdufis6v8$h$is_^hne88v-)k0%a-!!*$!ywgr'

DEBUG = True

ALLOWED_HOSTS = ['192.168.0.2', '192.168.0.3', 'app-store.ks.ua', '0.0.0.0', '185.253.218.184', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'store',
        'USER': 'appstoredb',
        'PASSWORD': 'appstore228',
        'HOST': 'local',
        'PORT': '5432',
    }
}
# STATIC_ROOT = (os.path.join(BASE_DIR, 'static'),)
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, 'media'),)

# STATIC_ROOT = '/home/www/shop/shop/static'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join('/home/www/shop/media')

CSRF_TRUSTED_ORIGINS = ['app-store.ks.ua']

