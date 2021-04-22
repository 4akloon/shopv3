import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['192.168.0.4', '192.168.0.3', 'app-store.ks.ua', '0.0.0.0', '185.253.218.184', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shop',
        'USER': 'appstoredb',
        'PASSWORD': 'appstore228',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# STATIC_ROOT = (os.path.join(BASE_DIR, 'static'),)
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, 'media'),)

STATIC_ROOT = '/home/www/shop/shop/static'
# STATICFILES_DIRS = (os.path.join('/home/www/shop/shop/static'),)

MEDIA_ROOT = os.path.join('/home/www/shop/media')

CSRF_TRUSTED_ORIGINS = ['app-store.ks.ua']

