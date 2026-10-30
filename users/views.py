from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomUserUpdatePassForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView, UpdateView

from .models import CustomUser


class UserRegisterView(CreateView):
    """Контроллер для регистрации пользователей"""
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')


class UserLogoutView(LogoutView):
    """Контроллер для выхода пользователя из системы - перенаправляет на главную"""


class UserProfileUpdateView(UpdateView):
    """Контроллер для редактирования профиля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'update_profile.html'

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.object.pk},
        )

class UserProfileUpdatePassView(PasswordChangeView):
    """Контроллер для изменения пароля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdatePassForm
    template_name = 'update_profile_pass.html'

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.request.user.pk},
        )