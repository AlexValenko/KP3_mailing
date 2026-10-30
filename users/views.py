from .forms import CustomUserCreationForm

from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView


class UserRegisterView(CreateView):
    """Контроллер для регистрации пользователей"""
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')


class UserLogoutView(LogoutView):
    """Контроллер для выхода пользователя из системы - перенаправляет на главную"""

