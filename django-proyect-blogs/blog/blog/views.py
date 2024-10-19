'''creacion de modulo views para realizar peticiones y respuestas a una pagina'''
'''a cada funcion dentro de este modulo se le denomina vista'''
'''el modulo views se vincula con el modulo urls, a cada funcion o respuesta o vista, se le
debera linkear/vincular un url para que pueda DEVOLVER la respuesta de forma visual en el navegador'''
#from django.http import HttpResponse
#import datetime
from django.views.generic import TemplateView

# SIEMPRE con httpresponse se recibe como parametro una request o solicitud
'''
def saludo(request):
    # tambien se puede definir una variable y llenarla de la cadena html correspondiente para su devolucion a django y esta lo devuelva 
    '''
'''documento = "<html> <head> <h1> Hola mundo </h1> </head> </html>" 
        return HttpResponse(documento)'''

'''
    #esto es un muestreo estatico
    return HttpResponse("hola mundo")# OJO PODEMOS ESCRIBIR EN HTML DENTRO DE LAS COMILLAS

# muestro dinamico
#muestra la fecha y hora actuales y se modifica en funcion de el momento de ejecucion

def darfecha (request):
    fechaActual=datetime.datetime.now()

    documento='''
''' <html>
            <body>
                <h1> Fecha actual es: %s
                </h1>
            </body>
        </html>'''
''' % fechaActual
    
    return HttpResponse(documento)

def calcularanio(request,anio):
    utilizando el url como obtencion de datos para realizar esta funcion, anio sera introducida en localHost/calcuarnio/2070
siendo 2070 el año en el que se quiera saber que edad tendra la persona, django trabaja con los url de manera tal de que
    todo lo que se escriba en la url del navegador lo toma como cadena de texto, por lo que o bien se lo formatea en la funcion en este
    mismo modulo o en la llamada a la vista en urls.py
    anio_act=2024
    anio_futuro=anio
    edad_actual=24
    edad_futura= edad_actual + (anio_futuro - anio_act)
    documento = 
        <html>
            <body>
                <h1> La edad que tendria una persona de 24 años en el año %s seria de: %s
                </h1>
            </body>
        </html> %(anio_act,edad_futura)
    return HttpResponse(documento)'''
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