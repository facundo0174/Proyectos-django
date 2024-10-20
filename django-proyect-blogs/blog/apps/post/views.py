from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView,DeleteView,UpdateView
from apps.post.models import Post, PostImage, Category, Comment
from apps.post.forms import NewPostForm, UpdatePostForm, CategoryForm, CommentForm
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Like, PostView
from django.views import View
from django.core.mail import send_mail
class PostUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'post/post_update.html'

    permission_required = 'post.change_post'  # El permiso segun signals.py

    def handle_no_permission(self):
        return super().handle_no_permission()#retorna 403

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['active_images'] = self.get_object().images.filter(active=True) # Pasamos las imágenes activas del post seleccionado a modificar
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
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)
        
        post.save() # Guardar el post finalmente
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("form_invalid is called")  # Print para depuración
        print(form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        # El reverse_lazy es para que no se ejecute hasta que se haya guardado el post
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.slug})
    
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post:category_recent')

    # Verificar el permiso adecuado
    permission_required = 'post.delete_post'  # El permiso que se requiere para eliminar posts

    # Sobrescribir el método para manejar cuando el usuario no tiene permisos
    def handle_no_permission(self):
        return super().handle_no_permission()

class PostListView(ListView):
    # esta view reprecenta la conjuncion de todas las categorias a la cual retorna la lista de post ordenado por fecha reciente
    model = Post
    template_name = 'post/category_recent.html'
    context_object_name = 'posts'
    paginate_by = 10  # Número de posts por página

    def get_queryset(self):
        order = self.request.GET.get('order', 'newest')  # Obtener el parámetro de orden
        queryset = Post.objects.order_by('-creation_date')# Ordenar por fecha (más reciente primero) esto sucede cuando se ingresa por primera vez
        if order == 'alphabetical':
            queryset = queryset.order_by('title')  # Ordenar alfabéticamente por título
        elif order == 'oldest':
            queryset = queryset.order_by('creation_date')  # Ordenar por fecha (más viejo primero)
        elif order == 'newest':
            queryset = queryset.order_by('-creation_date') # Ordenar por fecha (más reciente primero)
        elif order == 'invert-alphabetical':
            queryset = queryset.order_by('-title') # Ordenar alfabéticamente inverso por título
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', 'newest')  # Añadir el orden al contexto
        return context

class TestView(ListView):
    model = Post
    template_name = 'post/test.html'  
    context_object_name = 'posts'
    paginate_by = 5  # Paginación de 5 elementos por página.

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            ).order_by('-creation_date')
        return Post.objects.all().order_by('-creation_date')  # Mostrar todos los posts si no hay búsqueda.

    def paginate_queryset(self, queryset, page_size):
        """ Sobrescribir paginación para manejar páginas vacías o inválidas. """
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # Si el número de página no es un entero, mostrar la primera página.
            page_obj = paginator.page(1)
        except EmptyPage:
            # Si la página está vacía, mostrar la última página válida.
            page_obj = paginator.page(paginator.num_pages)

        return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())

class PostCreateView(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'post/post_create.html'

    permission_required = 'post.add_post'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        images = self.request.FILES.getlist('images')
        PostImage.objects.filter(post=post).delete() #solucion a img defecto duplicada

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
        
        # Incrementar contador de visualizaciones solo si el usuario no ha visto el post antes
        if self.request.user.is_authenticated:
            view_exists = PostView.objects.filter(user=self.request.user, post=self.object).exists()
            if not view_exists:
                PostView.objects.create(user=self.request.user, post=self.object)
                self.object.views += 1
                self.object.save()

        # Obtener todas las imágenes activas del post
        active_images = self.object.images.filter(active=True) 
        context['active_images'] = active_images
        context['add_comment_form'] =  CommentForm()
        context ['user'] = self.request.user #obtengo usuario autenticado para comprobacion a nivel template
        context['add_comment_form'] = CommentForm()
   
        # Obtener el estado del "me gusta" para el usuario actual
        if self.request.user.is_authenticated:
            user_like = Like.objects.filter(user=self.request.user, post=self.object).exists()
            context['user_like'] = user_like

        # Obtener la cantidad total de "me gusta"
        context['likes_count'] = self.object.likes  # Asumiendo que `likes` es un campo IntegerField en tu modelo Post

        # Editar comentario
        edit_comment_id = self.request.GET.get('edit_comment')
        if edit_comment_id:
            comment = get_object_or_404(Comment, id=edit_comment_id)
            # Permitimos editar solo si el usuario logueado es el autor del comentario
            if comment.author == self.request.user:
                context['editing_comment_id'] = comment.id
                context['edit_comment_form'] = CommentForm(instance=comment)
            else:
                context['editing_comment_id'] = None
                context['edit_comment_form'] = None
        #empieza la linea no borrada del merge que se asegura de el autor es el que trata de borrar y lo que se quiera borrar no sea un SU o collaborator
        # Eliminar comentario
        delete_comment_id = self.request.GET.get('delete_comment')
        if delete_comment_id:
            comment = get_object_or_404(Comment, id=delete_comment_id)
            # Permitimos solo si el usuario logueado tiene permiso para eliminar el comentario TODO: accion colaborador no esta
            if ( comment.author == self.request.user or (comment.post.author == self.request.user and not comment.author.is_admin and not comment.author.is_superuser) or self.request.user.is_superuser or self.request.user.groups.filter( name='administrator').exists()):
                        # Es autor del comentario, Es autor del post, pero el comentario no es de un admin o un superuser
                context['deleting_comment_id'] = comment.id
            else:
                context['deleting_comment_id'] = None
         #termina la linea no borrada

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        # Manejar el "me gusta"
        if request.user.is_authenticated:
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if created:
                # Si el "me gusta" no existía, se creó uno nuevo
                post.likes += 1
            else:
                # Si ya existía, lo eliminamos (el usuario "retira" su "me gusta")
                like.delete()
                post.likes -= 1

            post.save()

        return redirect('post:post_detail', slug=post.slug)

class CategoryListView(ListView):
    model = Category
    template_name = 'post/category_list.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_queryset(self):
        # Devuelve las categorías ordenadas alfabéticamente
        return Category.objects.order_by('category_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        #context ['user'] = self.request.user #obtengo usuario autenticado para comprobacion a nivel template
        #estaba en desarrollo no se sabe porque no se lo incorpora ['user']
        # No es necesario volver a obtener las categorías aquí razon lo hace el queryset

        return context

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'post/category_create.html'
    success_url = reverse_lazy('index')
    permission_required = 'post.add_category'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403

    def form_valid(self, form):
        
        #usamos orm django para buscar en la bd datos que coincidan, si coincide retorna errores y no guarda
        if Category.objects.filter(category_name = form.cleaned_data['category_name']).exists():
            return self.form_invalid(form)  # Devuelve el formulario con error
        
        return super().form_valid(form)#solo guarda si no encuentra coincidencias

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'post/category_update.html'
    success_url = reverse_lazy('index')
    permission_required = 'post.change_category'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403

    def form_valid(self, form):
        
        #usamos orm django para buscar en la bd datos que coincidan, si coincide retorna errores y no guarda
        if Category.objects.filter(category_name = form.cleaned_data['category_name']).exists():
            form.add_error('category_name', 'Ya existe una categoría con este nombre.')
            return self.form_invalid(form)  # Devuelve el formulario con error
        
        return super().form_valid(form)#solo guarda si no encuentra coincidencias
    
    def form_invalid(self, form):
        print('entro por formulario invalido el error es el siguietnt')
        print(form.errors)
        return super().form_invalid(form)

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Category
    template_name = 'post/category_delete.html'
    success_url = reverse_lazy('index')
    permission_required = 'post.delete_category'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403

class PostByCategoryView(ListView):
    model = Post
    template_name = 'post/post_by_category.html'
    context_object_name = 'posts'
    paginate_by = 5  # Asegúrate de incluir esta línea

    def get_queryset(self):
        #obtengo valores de evaluacion del contexto antes de evaluar y renderizar pagina por el url para tomar accion
        queryset = super().get_queryset() 
        # obtego el slug reprecentante de la categoria
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug) #busco la categoria o da error
        queryset = Post.objects.filter(category=category) #ordeno antes de mostrar la vista por categoria los post
        # a partir de aca ordena por fecha o nombre
        order = self.request.GET.get('order', 'newest')  # Obtener el parámetro de orden
        if order == 'alphabetical':
            queryset = queryset.order_by('title')  # Ordenar alfabéticamente por título
        elif order == 'oldest':
            queryset = queryset.order_by('creation_date')  # Ordenar por fecha (más viejo primero)
        elif order == 'invert-alphabetical':
            queryset = queryset.order_by('-title') # Ordenar alfabéticamente inverso por título
        else:
            queryset = queryset.order_by('-creation_date') # Ordenar por fecha (más reciente primero)
        
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()  # Agrega todas las categorías al contexto
        context['order'] = self.request.GET.get('order', 'newest')  # Añadir el orden al contexto
        context ['user'] = self.request.user #obtengo usuario autenticado
        return context

class AcercaDe(TemplateView):
    template_name='post/acerca_de.html'

class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'
    permission_required = 'post.add_comment'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug':self.object.post.slug})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'
    login_url = reverse_lazy('user:auth_login')
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['pk']) 
        #busco el comentario en la tabla BD del post, con el ID segun a modificar
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug':self.object.post.slug})
    
    def test_func(self): #prueba de acceso para los objetos, en este caso el comentario seleccionado a editar/eliminar
        comment = self.get_object()#si es el mismo autor entonces permite modificar/eliminar, sino tira error
        return comment.author == self.request.user
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy('user:auth_login')
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug':self.object.post.slug})
    
    def test_func(self):
        #aqui la prueba se complejiza ya que compueba los permisos y grupos para la eliminacion
        comment = self.get_object()
        is_comment_author = self.request.user == comment.author
        is_post_author = (self.request.user == comment.post.author and not comment.author.is_admin and not comment.author.is_superuser)
        is_admin = self.request.user.is_superuser or self.request.user.groups.filter(name='administrator').exists()

        return is_comment_author or is_post_author or is_admin

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')  # Asegúrate de tener este archivo en templates

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Configura el correo
        subject = f"Nuevo mensaje de {name}"
        body = f"Nombre: {name}\nEmail: {email}\nMensaje: {message}"
        from_email = settings.EMAIL_HOST_USER  # Tu correo de Gmail
        to_email = settings.ADMIN_EMAIL  # Correo del administrador

        send_mail(subject, body, from_email, [to_email])

        return redirect('post:thanks')  # Redirige a la página de agradecimiento