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
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border border-gray-400 rounded-md py-2 px-3 text-slate-800',
            'placeholder': 'Contraseña'
        }),
    )

