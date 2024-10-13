from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from apps.user.forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from apps.user.models import usuario
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin,DetailView):
    model = usuario
    template_name='user/user_profile.html'
    context_object_name='user'
    login_url = reverse_lazy('user:auth_login')


    def get_object(self):
        #obtengo el id de usuario del url, y busco en la BD el objeto usuario segun el modelo usuario de la tabla y lo traigo
        pk = self.kwargs['pk']
        return get_object_or_404(usuario, pk=pk)
    
class UserUpdateView(UpdateView):
    template_name='user/user_update.html'

class UserDeleteView(DeleteView):
    template_name='user/user_delete.html'

class RegisterView(CreateView):
    template_name = 'auth/auth_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index') # Redirige al home una vez registrado
    
    def form_valid(self, form):
        # Llama a la función form_valid de la clase padre y guarda el usuario
        response = super().form_valid(form)
        # Asignar el grupo Registered al usuario recién creado
        registered_group = Group.objects.get(name='registred')
        self.object.groups.add(registered_group)
        # En caso de ser necesario se le puede asignar explicitamente los permisos del grupo al usuario
        # for permission in registered_group.permissions.all():
        # self.object.user_permissions.add(permission)
        return response

class LoginView(LoginViewDjango):
    template_name = 'auth/auth_login.html'
    authentication_form = LoginForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        
        return reverse_lazy('home')
    
class LogoutView(LogoutViewDjango):
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        
        return reverse_lazy('home')
    
