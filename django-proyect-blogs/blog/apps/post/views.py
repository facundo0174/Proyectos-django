from django.views.generic import TemplateView, ListView, DetailView, CreateView
from apps.post.models import Post, PostImage
from apps.post.forms import NewPostForm
from django.urls import reverse
from django.conf import settings


class DetallePostView(TemplateView):
    template_name='post/post_detail.html'

class PostUpdateView(TemplateView):
    template_name='post/post_Update.html'

class PostDeleteView(TemplateView):
    template_name='post/post_delete.html'

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

