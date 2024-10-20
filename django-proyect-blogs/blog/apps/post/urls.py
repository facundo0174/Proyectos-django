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
    path('posts/<slug:slug>/',vistaPost.PostDetailView.as_view(),name='post_detail'),
    path('posts/<slug:slug>/update/',vistaPost.PostUpdateView.as_view(),name='post_update'),
    path('posts/<slug:slug>/delete/',vistaPost.PostDeleteView.as_view(),name='post_delete'),
    path('category/new/',vistaPost.CategoryCreateView.as_view(),name='category_create'),
    path('category/edit/',vistaPost.CategoryListView.as_view(),name='category_list'),
    path('category/<slug:slug>/update/',vistaPost.CategoryUpdateView.as_view(),name='category_update'),
    path('category/<slug:slug>/delete/',vistaPost.CategoryDeleteView.as_view(),name='category_delete'),
    path('category/recientes/', vistaPost.PostListView.as_view(), name='category_recent'),
    path('category/<slug:slug>/',vistaPost.PostByCategoryView.as_view(),name='post_by_category'),
    path('post/<slug:slug>/comment/create/',vistaPost.CommentCreateView.as_view(),name='comment_create'),
    path('comments/<uuid:pk>/update/', vistaPost.CommentUpdateView.as_view(),name='comment_update'),
    path('comments/<uuid:pk>/delete/', vistaPost.CommentDeleteView.as_view(),name='comment_delete'),
    path('test/', vistaPost.TestView.as_view(), name='test_view'),
]

