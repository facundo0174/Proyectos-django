from django.db import models
import uuid
from django.conf import settings
#import datetime se puede usar tambien
from django.utils import timezone#devuelve la fecha y hora
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, max_length=200)
    content =  models.TextField(max_length=3000)#contenido del post
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    # si quieres eliminar todos los post al eliminar usuario se coloca: on_delete=models.CASCADE, para que no muestre user al elimnar, on_delete=setnull
    creation_date=models.DateTimeField(default=timezone.now)
    modification_date=models.DateTimeField(auto_now=True)
    allowed_comments=models.BooleanField(default=True)

    def __str__(self):
        return(self.title)
    

    @property
    def amount_comments(self):
        return (self.comments.count()) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=self.generate_unique_slug()
        
        super().save(*args,**kwargs)
        #TODO = definir safe para imagenes

    def generate_unique_slug(self):
        #se realizara los siguiente
        # esto es un titulo
        # esto-es-un-titulo
        #por lo que se convertira en: localhost/posts/esto-es-un-titulo
        slug = slugify(self.title)
        unique_slug = slug
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num+=1
        return unique_slug

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    content= models.TextField(max_length=500)
    creation_date=models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")

    def __str__(self): #esto provoca que cuando se llame al objeto muestre el contenido o x cosa
        return (self.content)


