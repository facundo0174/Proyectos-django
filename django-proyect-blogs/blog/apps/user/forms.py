from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.user.models import usuario

class RegisterForm(UserCreationForm):
    class Meta:
        model = usuario
        fields = ('username', 'email', 'alias', 'avatar')

