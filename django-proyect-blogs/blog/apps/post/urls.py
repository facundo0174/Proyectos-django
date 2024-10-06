from django.urls import path
import apps.post.views as vistaPost

#si tienes una view como clase debes hace as view() siempre
app_name = 'post'
'''
MUCHO OJO EL ORDEN IMPORTA YA QUE EVALUA SEGUN EL ORDEN; SI HAY SOLO SLUGS ENTRARA SIEMPRE
EJEMPLO: acerca_de y detalle por mas que evalues acerca_de si detalle esta primero 
siempre mostrara detalle lo cual es incorrecto si presionas el detalle.
'''

urlpatterns = [
    path('posts/acerca-de/',vistaPost.AcercaDe.as_view(),name='acerca_de'),
    path('post/create/',vistaPost.PostCreateView.as_view(),name='post_create'),
    path('posts/<slug:slug>/',vistaPost.DetallePostView.as_view(),name='post_detail'),
    path('posts/<slug:slug>/update/',vistaPost.PostUpdateView.as_view(),name='post_update'),
    path('posts/<slug:slug>/delete/',vistaPost.PostDeleteView.as_view(),name='post_delete'),
    path('posts/seccion1/<slug:slug>/',vistaPost.SeccionAvances.as_view(),name='seccion_avances_tegnologicos'),
    path('posts/seccion2/<slug:slug>/',vistaPost.SeccionComponentes.as_view(),name='seccion_componentes'),
    path('posts/seccion3/<slug:slug>/',vistaPost.SeccionEmpresas.as_view(),name='seccion_empresas'),
    path('posts/seccion4/<slug:slug>/',vistaPost.SeccionIA.as_view(),name='seccion_IA'),
    path('posts/seccion5/<slug:slug>/',vistaPost.SeccionProgramacion.as_view(),name='seccion_programacion'),
    path('posts/seccion6/<slug:slug>/',vistaPost.SeccionTendencias.as_view(),name='seccion_tendencias'),
    
]

