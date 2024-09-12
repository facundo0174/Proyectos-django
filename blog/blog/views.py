'''creacion de modulo views para realizar peticiones y respuestas a una pagina'''
'''a cada funcion dentro de este modulo se le denomina vista'''
'''el modulo views se vincula con el modulo urls, a cada funcion o respuesta o vista, se le
debera linkear/vincular un url para que pueda DEVOLVER la respuesta de forma visual en el navegador'''
from django.http import HttpResponse
import datetime
# SIEMPRE con httpresponse se recibe como parametro una request o solicitud

def saludo(request):
    # tambien se puede definir una variable y llenarla de la cadena html correspondiente para su devolucion a django y esta lo devuelva 
    '''
        documento = "<html> <head> <h1> Hola mundo </h1> </head> </html>" 
        return HttpResponse(documento)

    '''
    #esto es un muestreo estatico
    return HttpResponse("hola mundo")# OJO PODEMOS ESCRIBIR EN HTML DENTRO DE LAS COMILLAS

# muestro dinamico

def darfecha (request):
    fechaActual=datetime.datetime.now()

    documento='''
        <html>
            <head>
                <h1> Fecha actual es: %s
                </h1>
            </head>
        </html>''' % fechaActual
    
    return HttpResponse(documento)


