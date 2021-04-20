import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['192.168.1.100', '192.168.0.77', 'app-store.ks.ua', '0.0.0.0', '185.253.218.184', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, '../media'),)

STATIC_ROOT = '/Users/genius/Documents/Dev/PycharmProjects/pythonProjectUA/shop/shop/static'
STATICFILES_DIRS = (os.path.join('/Users/genius/Documents/Dev/PycharmProjects/pythonProjectUA/shop/static'),)

MEDIA_ROOT = os.path.join('/Users/genius/Documents/Dev/PycharmProjects/pythonProjectUA/media')

CSRF_TRUSTED_ORIGINS = ['app-store.ks.ua', '192.168.0.77', '0.0.0.0']

