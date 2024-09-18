import os
from dotenv import load_dotenv

load_dotenv()
print("se uso settings ")
DJANGO_ENV = os.getenv('DJANGO_ENV','development')
print(f"\nentorno en: {DJANGO_ENV}\n")
if DJANGO_ENV == 'production':
    print("cargando prod")
    from .configurations.production import *
else:
    print("cargando local")
    from .configurations.local import *

