from django.views.generic import TemplateView

class UserProfileView(TemplateView):
    template_name='user/user_profile.html'

class UserUpdateView(TemplateView):
    template_name='user/user_update.html'

class UserDeleteView(TemplateView):
    template_name='user/user_delete.html'
# Create your views here.

class UserCreateView(TemplateView):
    template_name='user/user_create.html'
