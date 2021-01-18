import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '7*jud^#yz+j0)9l)#py(*2un&7!%x)ob&d@rc$p%k8swsr_ngx'

DEBUG = True

ALLOWED_HOSTS = ['192.168.0.2', '192.168.0.3', 'app-store.ks.ua', '0.0.0.0', '185.253.218.184', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# STATIC_ROOT = (os.path.join(BASE_DIR, 'static'),)
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, 'media'),)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# STATIC_ROOT = '/home/www/shop/shop/static'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, '../static')

CSRF_TRUSTED_ORIGINS = ['app-store.ks.ua']

