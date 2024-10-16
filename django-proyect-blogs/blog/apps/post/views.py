from django.views.generic import TemplateView, ListView, DetailView, CreateView,DeleteView,UpdateView
from apps.post.models import Post, PostImage, Category, Comment
from apps.post.forms import NewPostForm, UpdatePostForm, CategoryForm, CommentForm
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin

class PostUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'post/post_update.html'

    permission_required = 'post.update_post_permission'  # El permiso segun signals.py

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
    permission_required = 'post.delete_post_permission'  # El permiso que se requiere para eliminar posts

    # Sobrescribir el método para manejar cuando el usuario no tiene permisos
    def handle_no_permission(self):
        return super().handle_no_permission()

class PostListView(ListView):
    # esta view reprecenta la conjuncion de todas las categorias a la cual retorna la lista de post ordenado por fecha reciente
    model = Post
    template_name = 'post/category_recent.html'
    context_object_name = 'posts'
    paginate_by = 5  # Número de posts por página

    def get_queryset(self):
        # Ordena los posts por fecha reciente y los retorna
        return Post.objects.order_by('-creation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()  # trae la lista de objetos ordenados en este caso los post al view como contexto para usarlos en el template
        # OJO solo a esta view los trae como contexto, si usaramos otra view este contexto de post ordenados por fecha desapareceria.
        return context

    
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'post/post_create.html'

    permission_required = 'post.create_post_permission'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
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

    def get_context_data(self, **kwargs): #obtengo datos del contexto basado en model=post, que serian los objetos de la tabla en BD
        context = super().get_context_data(**kwargs)
        # Obtener todas las imágenes activas del post
        active_images = self.object.images.filter(active=True) 
        #filtro las img del post, el contexto es de un unico post, ya que poseen slugs unicos, por lo tanto postDetail hace referencia
        #a la vista de 1 solo objeto post, al hacer contexto tomamos ese objeto unico post de la BD y buscamos las img para mostrar.
        # las cuales son asociadas por otra tabla por ello referenciamos como contexto IMAGES, ya que puede tener muchas.
        context['active_images'] = active_images
        context['add_comment_form'] =  CommentForm()
        context ['user'] = self.request.user #obtengo usuario autenticado para comprobacion a nivel template
        
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
        context ['user'] = self.request.user #obtengo usuario autenticado para comprobacion a nivel template
        return context

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'post/category_create.html'
    success_url = reverse_lazy('index')
    permission_required = 'post.create_category_permission'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    
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
    permission_required = 'post.update_post_permission'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
    def handle_no_permission(self):
        return super().handle_no_permission()#retorna error 403

    def form_valid(self, form):
        
        #usamos orm django para buscar en la bd datos que coincidan, si coincide retorna errores y no guarda
        if Category.objects.filter(category_name = form.cleaned_data['category_name']).exists():
            form.add_error('category_name', 'Ya existe una categoría con este nombre.')
            return self.form_invalid(form)  # Devuelve el formulario con error
        
        return super().form_valid(form)#solo guarda si no encuentra coincidencias

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Category
    template_name = 'post/category_delete.html'
    success_url = reverse_lazy('index')
    permission_required = 'post.delete_post_permission'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
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
        # obtengo el string asociado a el orden, si no existe devuelve recientes como valor por defecto
        #este recientes es de post por fecha reciente, el caso de categoria recientes es uno muy especifico
        orden = self.request.GET.get('orden', 'Recientes')
        # obtego el slug reprecentante de la categoria
        category_slug = self.kwargs['slug']

        if category_slug == 'Recientes': #sencible a mayusculas y minusculas
            return Post.objects.all().order_by('-creation_date') #ordeno a todos por fecha reciente
        else:# ordena/filtra por categoria
            category = get_object_or_404(Category, slug=category_slug) #busco la categoria o da error
            queryset = Post.objects.filter(category=category) #ordeno antes de mostrar la vista por categoria los post
            # a partir de aca ordena por fecha o nombre
            if orden == 'Reciente':
                queryset = queryset.order_by('-creation_date')
            elif orden == 'Antiguo':
                queryset = queryset.order_by('creation_date')
            elif orden == 'Alfabetico-ascendente':
                queryset = queryset.order_by('title')
            elif orden == 'Alfabetico-descendente':
                queryset = queryset.order_by('-title')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['categories'] = Category.objects.all()  # Agrega todas las categorías al contexto
        context['orden']= self.request.GET.get('orden','Recientes')
        context ['user'] = self.request.user #obtengo usuario autenticado
        return context


class AcercaDe(TemplateView):
    template_name='post/acerca_de.html'

class Recent_Post_View(ListView):
    model = Post
    template_name = 'post/category_recent.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['user'] = self.request.user #obtengo usuario autenticado para comprobacion a nivel template
        return context

    def get_queryset(self):
        #retorno una lista  de objetos post ordenados por fecha reciente
        return Post.objects.all().order_by('-creation_date') #ordeno a todos por fecha reciente

class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'
    permission_required = 'post.create_post_permission'  # El permiso segun lo_que_modifica.nombre_permiso_de_signals
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

