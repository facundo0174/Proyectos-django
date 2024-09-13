import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.getenv('DJANGO_ENV','development')

if DJANGO_ENV == 'production':
    from .blog.configurations.production import *
else:
    from .blog.configurations.local import *