from django.urls import path
import apps.post.views as vistaPost
#si tienes una view como clase debes hace as view() siempre
app_name = 'post'
urlpatterns = [
    path('posts/<slug:slug>/',vistaPost.DetallePostView.as_view(),name='post_detail'),
    path('posts/<slug:slug>/update/',vistaPost.PostUpdateView.as_view(),name='post_update'),
    path('posts/<slug:slug>/delete/',vistaPost.PostDeleteView.as_view(),name='post_delete'),
    path('posts/<slug:slug>/create/',vistaPost.PostDeleteView.as_view(),name='post_create'),
]
