from django.db import models
import uuid
from django.conf import settings
#import datetime se puede usar tambien
from django.utils import timezone#devuelve la fecha y hora
from django.utils.text import slugify
import os
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,unique=True)
    category_name = models.CharField (max_length=50, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField (unique=True, null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return(self.category_name)
    

class Post(models.Model):
    
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True, max_length=200)
    content =  models.TextField(max_length=3000)#contenido del post
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    # si quieres eliminar todos los post al eliminar usuario se coloca: on_delete=models.CASCADE, para que no muestre user al elimnar, on_delete=setnull
    creation_date=models.DateTimeField(default=timezone.now)
    modification_date=models.DateTimeField(auto_now=True)
    allowed_comments=models.BooleanField(default=True,editable=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="category", null=False)#se utilizara para obtener todos los post de x categoria segun lo nescesario
    # CATEGORY DEBE SER SI O SI FALSE; PERO SE DEJO EN TRUE PARA REALIZAR UN PEQUEÑO MIGRATE DE PRUEBA
    views = models.IntegerField(default=0)  # Contador de visualizaciones
    likes = models.IntegerField(default=0)   # Contador de me gusta
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return(self.title)
    

    @property
    def amount_comments(self):
        return (self.comments.count()) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=self.generate_unique_slug()
        
        super().save(*args,**kwargs)
        
        if not self.images.exists():
            PostImage.objects.create(post=self,image="post/default/post_default.png")

    def generate_unique_slug(self):
        #se realizara los siguiente
        # esto es un titulo
        # esto-es-un-titulo
        #por lo que se convertira en: localhost/posts/esto-es-un-titulo
        slug = slugify(self.title)
        unique_slug = slug
        num=0
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num+=1
        return unique_slug
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Asegura que cada usuario solo pueda dar un "me gusta" por post

class PostView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    content= models.TextField(max_length=500)
    creation_date=models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")

    def __str__(self): #esto provoca que cuando se llame al objeto muestre el contenido o x cosa
        return (self.content)

def get_image_filename(instance,filename):    
    _, base_fileExtension= os.path.splitext(filename)
    images_count=instance.post.images.count()
    new_fileName = f"post_{instance.post.id}_coverImage_{images_count + 1}{base_fileExtension}"
    
    return os.path.join('post/cover',new_fileName)

class PostImage(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename,default='post/default/post_default.png')
    active = models.BooleanField(default=True)
    creation_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"postImage:{self.id}"
    
