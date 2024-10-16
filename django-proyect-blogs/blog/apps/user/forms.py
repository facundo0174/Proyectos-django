from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import usuario

class RegisterForm(UserCreationForm):
    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias', 'avatar')

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),)
    password = forms.CharField(widget=forms.PasswordInput (attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),)
    # Django form trabaja con widgets
    # Los widgets son los elementos que se renderizan en el HTML
    # Pueden recibir atributos como clases, id, placeholder, etc
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias')

    def clean_username(self):
        username = self.cleaned_data.get('username') #obtengo el contenido actual del username de usuario models.py
        current_username = self.instance.username  # El nombre de usuario actual

        # Si el nuevo username es el mismo que el actual, no validamos
        if username == current_username:
            return username
        
        # Si hay un usuario con el mismo username
        if usuario.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        
        return username

    def clean_alias(self):
        alias = self.cleaned_data.get('alias') # alias encontrado en el campo de validacion de el formulario contextual
        current_alias = self.instance.alias  # El alias actual

        # Si el nuevo alias es el mismo que el actual, no validamos
        if alias == current_alias:
            return alias
        
        # Si hay un usuario con el mismo alias
        if usuario.objects.exclude(pk=self.instance.pk).filter(alias=alias).exists():
            raise forms.ValidationError("Este alias ya está en uso.")
        
        return alias

