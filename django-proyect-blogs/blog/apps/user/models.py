from django.contrib.auth.models import AbstractUser #clase modelo para usuario django que se agrega a su base de datos sqlite3 o cual sea con la que trabaja
from django.db import models
import os
import uuid

def get_avatar_filename(instance,filename):#la instancia y el archivo lo esta pasando el usuario
    #recibo image124123.jpg y divido la extencion por un lado y el nombre por el otro
    
    base_fileName, base_fileExtension= os.path.splitext(filename)
    new_fileName = f"user_{instance.id}_avatar{base_fileExtension}"
    
    return os.path.join('user/avatar',new_fileName)


class usuario(AbstractUser):
    
    alias = models.CharField(max_length=30 , default= None, null=True,blank=True) #equivalente a VARCHAR con restricion 30 caracteres y posibilidad de estar en blanco
    avatar = models.ImageField(upload_to=get_avatar_filename, default='user/default/avatar_default.jpg')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    
    @property
    def is_collaborator(self):
        return self.groups.filter(name='collaborators').exists()
    
    @property
    def is_admin(self):
        return self.groups.filter(name='administrator').exists()
    
    @property
    def is_registered(self):
        return self.groups.filter(name='registred').exists()
