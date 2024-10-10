from django import forms
from apps.post.models import Post, PostImage, Category, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category','title', 'content', 'allowed_comments')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
        labels ={'category_name':'Nombre de Categoria',}
        error_messages = {'category_name': {'unique': 'Ya existe una categoría con este nombre. intentalo nuevamente'},}

class NewPostForm(PostForm):
    image = forms.ImageField(required=False)
    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data['image']
        if commit:
            post.save()
            if image:
                PostImage.objects.create(post=post, image=image)
        return post

class UpdatePostForm(PostForm):
    image = forms.ImageField(required=False)
    print('entro en el post update')
    def __init__(self, *args, **kwargs):
        print('entro en el init')
        # Obtenemos las imágenes activas del post que se quiere actualizar
        self.active_images = kwargs.pop('active_images', None)
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        
        if self.active_images:
            for image in self.active_images:
                # keep_image_1, keep_image_2, ... etc es el nombre del campo que se creará en el formulario para mantener la imagen activa
                field_name = f"keep_image_{image.id}"
                self.fields[field_name] = forms.BooleanField(required=False, initial=True, label=f"Mantener {image}")
    
    def save(self, commit=True):
        post = super().save(commit=False) #guardamos los cambios en los campos de post pero no definitivamente en bd
        print('entro en el save')
        if commit:
            post.save()
            print('entro en el if commit')
            new_images = self.files.getlist('images') # si agregamos nuevas imagenes, el nombre sera igual al del template utilizado para referenciar a los campos input
            
            if new_images:
                print('entro en el si hay imagenes nuevas')
                for image in new_images:
                    PostImage.objects.create(post=post, image=image)
                    
            #if self.cleaned_data['image']: # Si el usuario sube una nueva imagen
            #   PostImage.objects.create(post=post, image=self.cleaned_data['image'])
            if self.active_images:
                print('entro en tratamiento de imagenes activas')
                for image in self.active_images:
                    if not self.cleaned_data.get(f"keep_image_{image.id}", True):
                        image.delete()
            '''if self.active_images: # Si hay imágenes activas y se quiere mantener alguna
                for image in self.active_images:
                    if not self.cleaned_data.get(f"keep_image_{image.id}", True):
                        image.delete() # Eliminar la imagen si el usuario no la quiere mantener, checkboxes desmarcados'''
        return post
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Comentario'}
        widgets = {'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario...', 'class': 'p-2'})}
