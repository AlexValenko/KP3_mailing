import secrets
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from mailing.models import MailingAttempt
from users.mixins import EmailVerifiedMixin

from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomUserUpdatePassForm, ResendVerificationForm
from .models import CustomUser


class UserRegisterView(CreateView):
    """Контроллер для регистрации пользователей"""

    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email_verified = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        self.object = user
        path = reverse(
            "users:email_confirm",
            kwargs={"token": token},
        )
        url = self.request.build_absolute_uri(path)
        send_mail(
            subject="Подтверждение почты",
            message=f"""Для подтверждения регистрации на сайте "Рассылка", перейдите по ссылке {url}.
            Если вы не регистрировались на этом сайте, проигнорируйте это письмо. Данное письмо не требует ответа""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                user.email,
            ],
        )

        return redirect(self.get_success_url())


def email_verification(request, token):
    """Функция верификации почты пользователя"""
    user = get_object_or_404(CustomUser, token=token)
    user.email_verified = True
    user.token = None
    user.save(update_fields=["email_verified", "token"])
    return redirect(reverse("users:login"))


class UserLogoutView(LogoutView):
    """Контроллер для выхода пользователя из системы - перенаправляет на главную"""


class UserProfileUpdateView(EmailVerifiedMixin, LoginRequiredMixin, UpdateView):
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


class UserProfileUpdatePassView(EmailVerifiedMixin, LoginRequiredMixin, PasswordChangeView):
    """Контроллер для изменения пароля пользователя"""

    form_class = CustomUserUpdatePassForm
    template_name = "update_profile_pass.html"

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_edit",
            kwargs={"pk": self.request.user.pk},
        )


class UserStatisticListView(EmailVerifiedMixin, LoginRequiredMixin, ListView):
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


class UserListView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс для отображения списка пользователей сайта (только для менеджеров)"""

    permission_required = "users.view_customuser"

    model = CustomUser
    template_name = "users_list.html"
    paginate_by = 20
    ordering = "email"
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(email__icontains=search_query)
        return queryset


class UserDetailView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс для отображения деталей пользователя сайта (только для менеджеров)"""

    permission_required = "users.view_customuser"

    model = CustomUser
    template_name = "users_detail.html"


class UserBlockView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """Действие по блокировке пользователя. Не дает заблокировать себя или суперпользователя"""

    permission_required = "users.block_user"

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if user == request.user or user.is_superuser:
            return HttpResponseRedirect(
                reverse(
                    "users:users_list",
                )
            )
        user.is_active = False
        user.save(update_fields=["is_active"])

        return HttpResponseRedirect(
            reverse(
                "users:users_list",
            )
        )


class UserUnblockView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """Действие по разблокировке пользователя"""

    permission_required = "users.block_user"

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = True
        user.save(update_fields=["is_active"])

        return HttpResponseRedirect(
            reverse(
                "users:users_list",
            )
        )


class ResendVerificationView(FormView):
    form_class = ResendVerificationForm
    template_name = "resend_verification.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email).first()

        if user is not None and user.is_active and not user.email_verified:
            token = secrets.token_hex(16)
            user.token = token
            user.save(update_fields=["token"])
            path = reverse(
                "users:email_confirm",
                kwargs={"token": token},
            )
            url = self.request.build_absolute_uri(path)

            try:
                result = send_mail(
                    subject="Подтверждение почты",
                    message=f"""Для подтверждения регистрации на сайте "Рассылка", перейдите по ссылке {url}.
                    Если вы не регистрировались на этом сайте, проигнорируйте это письмо.
                    Данное письмо не требует ответа""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[
                        user.email,
                    ],
                )
                if result != 1:
                    form.add_error(None, "Не удалось отправить письмо. Попробуйте позже.")
                    return self.form_invalid(form)
            except (SMTPException, OSError) as e:
                form.add_error(None, f"Не удалось отправить письмо: {e}")
                return self.form_invalid(form)

        messages.info(
            self.request,
            "Если для этого адреса есть активный аккаунт "
            "с неподтверждённой почтой, мы отправили письмо. "
            "Проверьте также папку «Спам».",
        )

        return super().form_valid(form)
