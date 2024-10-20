'''creacion de modulo views para realizar peticiones y respuestas a una pagina'''
'''a cada funcion dentro de este modulo se le denomina vista'''
'''el modulo views se vincula con el modulo urls, a cada funcion o respuesta o vista, se le
debera linkear/vincular un url para que pueda DEVOLVER la respuesta de forma visual en el navegador'''
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from apps.post.models import Post, Category  # Asegúrate de importar tu modelo Post

class VistaIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtiene el post destacado
        context['featured_post'] = Post.objects.filter(is_featured=True).first()
       
        # Obtiene los dos posts más populares basados en "likes"
        context['popular_posts'] = Post.objects.order_by('-likes')[:2]
        
        # Obtiene los seis posts más recientes
        context['recent_posts'] = Post.objects.order_by('-creation_date')[:6]
        
        # Obtiene todas las categorías para mostrarlas en el contexto
        context['categories'] = Category.objects.all()  # Obtiene todas las categorías

        # Filtra los posts por categoría si se especifica
        category_slug = self.request.GET.get('category_slug')
        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug)
            context['category_posts'] = Post.objects.filter(category=selected_category).order_by('-creation_date')
        else:
            context['category_posts'] = Post.objects.none()  # No muestra posts si no hay categoría seleccionada

        return context

# Es importante que el argumento exception esté presente para que Django lo pueda identificar como un manejador de errores

def not_found_view(request, exception):
    return render(request, 'errors/error_not_found.html', status=404)
def internal_error_view(request):
    return render(request, 'errors/error_internal.html', status=500)
def forbidden_view(request, exception):
    return render(request, 'errors/error_forbidden.html', status=403)
