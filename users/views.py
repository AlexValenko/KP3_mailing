from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования профиля пользователя"""

    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "update_profile.html"

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.object.pk},
        )


class UserProfileUpdatePassView(LoginRequiredMixin, PasswordChangeView):
    """Контроллер для изменения пароля пользователя"""

    form_class = CustomUserUpdatePassForm
    template_name = "update_profile_pass.html"

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.request.user.pk},
        )


class UserStatisticListView(LoginRequiredMixin, ListView):
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


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс для отображения списка пользователей сайта (только для менеджеров)"""
    permission_required = "users.view_customuser"

    model = CustomUser
    template_name = "users_list.html"
    paginate_by = 20
    ordering = "email"
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(email__icontains=search_query)
        return queryset


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс для отображения деталей пользователя сайта (только для менеджеров)"""
    permission_required = "users.view_customuser"

    model = CustomUser
    template_name = "users_detail.html"


class UserBlockView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "users.block_user"

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = False
        user.save(update_fields=["is_active"])

        return HttpResponseRedirect(
            reverse("users:users_list",)
        )

class UserUnblockView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "users.block_user"

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = True
        user.save(update_fields=["is_active"])

        return HttpResponseRedirect(
            reverse("users:users_list", )
        )