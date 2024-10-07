from django.views.generic import TemplateView, ListView, DetailView, CreateView,DeleteView,UpdateView
from apps.post.models import Post, PostImage
from apps.post.forms import NewPostForm, UpdatePostForm
from django.urls import reverse,reverse_lazy
from django.conf import settings


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
    success_url = reverse_lazy('post:post_list')

class PostCreateView(TemplateView):
    template_name='post/post_create.html'

class SeccionIA(TemplateView):
    template_name='post/seccion_IA.html'

class SeccionAvances(TemplateView):
    template_name='post/seccion_avances_tegnologicos.html'

class SeccionComponentes(TemplateView):
    template_name='post/seccion_componentes.html'

class SeccionEmpresas(TemplateView):
    template_name='post/seccion_empresas.html'

class SeccionProgramacion(TemplateView):
    template_name='post/seccion_programacion.html'

class SeccionTendencias(TemplateView):
    template_name='post/seccion_tendencias.html'

class AcercaDe(TemplateView):
    template_name='post/acerca_de.html'

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'

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
    




