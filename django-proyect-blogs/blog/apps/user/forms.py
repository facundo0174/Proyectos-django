from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import usuario

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',  # Estilo del marco
            'placeholder': 'Contraseña'
        }),
        help_text="Su contraseña debe contener al menos 8 caracteres."
    )
    
    password2 = forms.CharField(
        label='Confirmación de contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',  # Estilo del marco
            'placeholder': 'Confirmar contraseña'
        }),
        help_text="Introduzca la misma contraseña nuevamente para verificar."
    )

    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',  # Estilo del marco para todos los campos
            })

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Verificar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        
        return cleaned_data


class LoginForm(AuthenticationForm):

        username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',
            'placeholder': 'Usuario'
        }),)
        password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',
            'placeholder': 'Contraseña'
        }),
    )
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias','avatar')

    def form_valid(self, form):

        if 'avatar' in self.request.FILES:
            avatar_file = self.request.FILES['avatar']

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


