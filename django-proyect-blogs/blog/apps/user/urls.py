from django.urls import path
import apps.user.views as vistaUser


#si tienes una view como clase debes hace as view() siempre
app_name = 'user'
urlpatterns = [
    path('users/profile/<uuid:pk>/',vistaUser.UserProfileView.as_view(),name='user_profile'),
    path('users/update/<uuid:pk>',vistaUser.UserUpdateView.as_view(),name='user_update'),
    path('users/delete/<uuid:pk>',vistaUser.UserDeleteView.as_view(),name='user_delete'),
    path('auth/register/',vistaUser.RegisterView.as_view(),name="auth_register"),
    path('auth/login/',vistaUser.LoginView.as_view(),name='auth_login'),
    path('auth/logout/',vistaUser.LogoutView.as_view(),name='auth_logout'),
]



