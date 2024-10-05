from django.urls import path
import apps.user.views as vistaUser


#si tienes una view como clase debes hace as view() siempre
app_name = 'user'
urlpatterns = [
    path('users/profile/',vistaUser.UserProfileView.as_view(),name='user_profile'),
    path('users/update/',vistaUser.UserUpdateView.as_view(),name='user_update'),
    path('users/delete/',vistaUser.UserDeleteView.as_view(),name='user_delete'),
    path('users/create/',vistaUser.UserCreateView.as_view(),name='user_create'),
    path('auth/register/',vistaUser.RegisterView.as_view(),name="auth_register"),
]



