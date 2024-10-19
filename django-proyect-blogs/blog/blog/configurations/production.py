from .base import *

DEBUG = False

ALLOWED_HOST = ['127.0.0.1','localhost','dominio-produccion.com']

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':os.getenv('DB_NAME'),
        'USER':os.getenv('DB_USER'),
        'PASSWORD':os.getenv('DB_PASSWORD'),
        'HOST':os.getenv('DB_HOST'),
        'PORT':os.getenv('DB_PORT'),
    }
}

os.environ['DJANGO_PORT'] = "8000"
