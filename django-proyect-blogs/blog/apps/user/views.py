from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from apps.user.forms import RegisterForm, LoginForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from apps.user.models import usuario
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

class UserProfileView(LoginRequiredMixin,DetailView):
    model = usuario
    template_name='user/user_profile.html'
    context_object_name='user'
    login_url = reverse_lazy('user:auth_login')
    #solo el usuario autenticado ACTUAL podra realizar esta vista, si quiere ver el perfil de otro usuario
    def get_object(self):
        #obtengo el id de usuario del url, y busco en la BD el objeto usuario segun el modelo usuario actual de la tabla y lo traigo
        user = self.request.user #esto me asegura que solo el propio usuario pueda ver su perfil y nadie mas
        return user
    
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = usuario
    form_class = UserUpdateForm
    context_object_name='user'
    login_url = reverse_lazy('user:auth_login')
    template_name='user/user_update.html'

    def get_object(self):
        #obtengo el id de usuario del url, y busco en la BD el objeto usuario segun el modelo usuario actual de la tabla y lo traigo
        user = self.request.user
        return user
    
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form_invalid is called")  # Print para depuración
        print(form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        # El reverse_lazy es para que no se ejecute hasta que se haya guardado el post
        return reverse_lazy('user:user_profile', kwargs={'pk': self.object.id})

class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = usuario
    template_name='user/user_delete.html'
    success_url = reverse_lazy('index')
    
    # aseguramos de que solo el usuario autenticado actual pueda eliminar la cuenta, osea a si mismo
    def get_object(self, queryset=None):
        return self.request.user

    # para no eliminarce a si mismo desde el template y eres administrador o colaborador
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        # Lógica adicional: asegurarse de que el usuario no sea un superusuario o tenga roles especiales
        if user.is_superuser or user.is_collaborator:
            return HttpResponseForbidden("No puedes eliminate eres superusuario/colaborador, contacta a administracion.")
        return super().delete(request, *args, **kwargs)

class RegisterView(CreateView):
    template_name = 'auth/auth_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')  # Redirige al home una vez registrado
    
    def form_valid(self, form):
        # Llama a la función form_valid de la clase padre y guarda el usuario
        response = super().form_valid(form)
        # Asignar el grupo Registered al usuario recién creado
        registered_group = Group.objects.get(name='registred')
        self.object.groups.add(registered_group)
        return response


class LoginView(LoginViewDjango):
    template_name = 'auth/auth_login.html'
    authentication_form = LoginForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        
        return reverse_lazy('index')
    
class LogoutView(LogoutViewDjango):
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('index')
    
