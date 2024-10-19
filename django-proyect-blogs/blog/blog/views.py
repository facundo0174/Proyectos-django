'''creacion de modulo views para realizar peticiones y respuestas a una pagina'''
'''a cada funcion dentro de este modulo se le denomina vista'''
'''el modulo views se vincula con el modulo urls, a cada funcion o respuesta o vista, se le
debera linkear/vincular un url para que pueda DEVOLVER la respuesta de forma visual en el navegador'''
#from django.http import HttpResponse
#import datetime
from django.views.generic import TemplateView
from django.shortcuts import render

class vistaindex(TemplateView):
        template_name='index.html'
        
#Es importante que el argumento exception esté presente
# para que Django lo pueda identificar como un manejador de errores

def not_found_view(request, exception):
    return render(request, 'errors/error_not_found.html', status=404)
def internal_error_view(request):
    return render(request, 'errors/error_internal.html', status=500)
def forbidden_view(request, exception):
    return render(request, 'errors/error_forbidden.html', status=403)
