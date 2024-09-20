from django.views.generic import TemplateView

class DetallePostView(TemplateView):
    template_name='post/post_detail.html'

class PostUpdateView(TemplateView):
    template_name='post/post_Update.html'

class PostDeleteView(TemplateView):
    template_name='post/post_delete.html'

class PostCreateView(TemplateView):
    template_name='post/post_create.html'