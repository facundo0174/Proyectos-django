from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView,DeleteView,UpdateView
from apps.post.models import Post, PostImage, Category
from apps.post.forms import NewPostForm, UpdatePostForm, CategoryForm
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class PostUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'post/post_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['active_images'] = self.get_object().images.filter(
        active=True) # Pasamos las imágenes activas
        return kwargs
    
    def form_valid(self, form):
        post = form.save(commit=False)
        active_images = form.active_images
        keep_any_image_active = False

        # Manejo de las imágenes activas
        if active_images:
            for image in active_images:
                field_name = f"keep_image_{image.id}"
                # Si el checkbox no está marcado, eliminamos la imagen
                if not form.cleaned_data.get(field_name, True):
                    image.active = False
                    image.save()
                else:
                    keep_any_image_active = True
                
        # Manejo de las nuevas imágenes subidas
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        # Si no se desea mantener ninguna imagen activa y no se subieron nuevas imágenes,se agrega una imagen por defecto
        if not keep_any_image_active and not images:
            PostImage.objects.create(
            post=post, image=settings.DEFAULT_POST_IMAGE)
        
        post.save() # Guardar el post finalmente
        return super().form_valid(form)
    
    def get_success_url(self):
        # El reverse_lazy es para que no se ejecute hasta que se haya guardado el post
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post:category_recent')

class PostCreateView(TemplateView):
    template_name='post/post_create.html'

class PostListView(ListView):
    model = Post
    template_name = 'post/category_recientes.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # Ordena las categorías alfabéticamente por el campo category_name pero la bd sigue desordenanda solo la vista es ordenada
        return Post.objects.order_by('-creation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()  # Asegúrate de que estás pasando las categorías
        return context
    
class PostCreateView(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'post/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        images = self.request.FILES.getlist('images')
    
        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        else:
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)
    
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todas las imágenes activas del post
        active_images = self.object.images.filter(active=True)
        context['active_images'] = active_images
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'post/category_list.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_queryset(self):
        # Ordena las categorías alfabéticamente por el campo category_name pero la bd sigue desordenanda solo la vista es ordenada
        return Category.objects.order_by('category_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Asegúrate de que estás pasando las categorías
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'post/category_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        
        #usamos orm django para buscar en la bd datos que coincidan, si coincide retorna errores y no guarda
        if Category.objects.filter(category_name = form.cleaned_data['category_name']).exists():
            return self.form_invalid(form)  # Devuelve el formulario con error
        
        return super().form_valid(form)#solo guarda si no encuentra coincidencias

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'post/category_update.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        
        #usamos orm django para buscar en la bd datos que coincidan, si coincide retorna errores y no guarda
        if Category.objects.filter(category_name = form.cleaned_data['category_name']).exists():
            form.add_error('category_name', 'Ya existe una categoría con este nombre.')
            return self.form_invalid(form)  # Devuelve el formulario con error
        
        return super().form_valid(form)#solo guarda si no encuentra coincidencias

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'post/category_delete.html'
    success_url = reverse_lazy('index')

class PostByCategoryView(ListView):
    model = Post
    template_name = 'post/post_by_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Obtén el slug de la URL y busca la categoría correspondiente
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        if category_slug == 'Recientes': #sencible a mayusculas y minusculas
            return Post.objects.all().order_by('-creation_date') #ordeno a todos por fecha reciente
        else:
            return Post.objects.filter(category=category).order_by('-creation_date') # ordeno segun categoria y por fecha reciente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()  # Agrega todas las categorías al contexto
        return context

class AcercaDe(TemplateView):
    template_name='post/acerca_de.html'

class Recent_Post_View(ListView):
    model = Post
    template_name = 'post/category_recent.html'
    context_object_name = 'posts'

    def get_queryset(self):
        #retorno una lista  de objetos post ordenados por fecha reciente
        return Post.objects.all().order_by('-creation_date') #ordeno a todos por fecha reciente
        