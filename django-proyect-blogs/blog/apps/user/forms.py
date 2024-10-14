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
    
class UpdateForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias')

