from django.views.generic import TemplateView

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