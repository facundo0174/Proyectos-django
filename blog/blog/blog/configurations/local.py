from .base import *
DEBUG = True

ALLOWED_HOST = ['127.0.0.1','localhost']

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':BASE_DIR / 'db.sqlite3'
    }
}

os.environ['DJANGO_PORT']='8000'
