from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from mailing.models import MailingAttempt

from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomUserUpdatePassForm
from .models import CustomUser


class UserRegisterView(CreateView):
    """Контроллер для регистрации пользователей"""

    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("users:login")


class UserLogoutView(LogoutView):
    """Контроллер для выхода пользователя из системы - перенаправляет на главную"""


class UserProfileUpdateView(UpdateView):
    """Контроллер для редактирования профиля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "update_profile.html"

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.object.pk},
        )


class UserProfileUpdatePassView(PasswordChangeView):
    """Контроллер для изменения пароля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdatePassForm
    template_name = "update_profile_pass.html"

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.request.user.pk},
        )


class UserStatisticListView(ListView):
    """Контроллер для показа статистики пользователя"""

    model = MailingAttempt
    context_object_name = "attempts"
    ordering = ("-attempted_at", "-pk")
    paginate_by = 20
    template_name = "user_statistic.html"

    def get_queryset(self):
        """Возвращает попытки, принадлежащие вошедшему пользователю"""
        return super().get_queryset().filter(mailing__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempts = self.object_list
        success_count = attempts.filter(status="success").count()
        failed_count = attempts.filter(status="failed").count()
        sent_messages_count = success_count

        context["user"] = self.request.user
        context["success_count"] = success_count
        context["failed_count"] = failed_count
        context["sent_messages_count"] = sent_messages_count

        return context
