from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from users.mixins import EmailVerifiedMixin


from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Message, Recipient
from .services import send_email


class HomeTemplateView(TemplateView):
    """Класс CBV для отображения домашней страницы - отображает статистику о рассылках и получателях"""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "home_statistics"
        data = cache.get(cache_key)

        if data is None:
            now = timezone.now()
            active_mailings = Mailing.objects.filter(
                status="started",
                start_datetime__lte=now,
                end_datetime__gte=now,
            )
            data = {
                "mailing_count": Mailing.objects.count(),
                "active_mailings_count": active_mailings.count(),
                "unique_recipients_count": Recipient.objects.count(),
            }

            cache.set(cache_key, data, timeout=60)
        context.update(data)
        return context

    # ----------------------- CRUD Recipient ------------------------------


class RecipientListView(EmailVerifiedMixin, LoginRequiredMixin, ListView):
    """Класс CBV для вывода списка получателей рассылки"""

    model = Recipient
    template_name = "recipient/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 30
    ordering = ("full_name",)

    def get_queryset(self):
        """Возвращает список получателей с учетом поиска."""
        if self.request.user.has_perm("mailing.view_all_recipients"):
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(owner=self.request.user)

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            queryset = queryset.filter(full_name__icontains=search_query)

        return queryset


class RecipientDetailView(EmailVerifiedMixin, LoginRequiredMixin, DetailView):
    """Класс CBV для просмотра детальной информации о получателе рассылки"""

    model = Recipient
    template_name = "recipient/recipient_detail_view.html"

    def get_queryset(self):

        if self.request.user.has_perm("mailing.view_all_recipients"):
            return super().get_queryset()

        return super().get_queryset().filter(owner=self.request.user)


class RecipientCreateView(EmailVerifiedMixin, LoginRequiredMixin, CreateView):
    """Класс CBV для создания получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(EmailVerifiedMixin, LoginRequiredMixin, UpdateView):
    """Класс CBV для редактирования получателя."""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class RecipientDeleteView(EmailVerifiedMixin, LoginRequiredMixin, DeleteView):
    """Класс CBV для удаления получателя."""

    model = Recipient
    template_name = "recipient/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# ----------------------- CRUD Message ------------------------------


class MessageListView(EmailVerifiedMixin, LoginRequiredMixin, ListView):
    """Класс CBV - выводит список сообщений"""

    model = Message
    template_name = "message/message_list.html"
    context_object_name = "messages"
    paginate_by = 30
    ordering = ("subject",)

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            queryset = queryset.filter(subject__icontains=search_query)

        return queryset


class MessageDetailView(EmailVerifiedMixin, LoginRequiredMixin, DetailView):
    """Класс CBV - выводит детали сообщения"""

    model = Message
    template_name = "message/message_detail_view.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageCreateView(EmailVerifiedMixin, LoginRequiredMixin, CreateView):
    """Класс CBV - для создания сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "message/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(EmailVerifiedMixin, LoginRequiredMixin, UpdateView):
    """Класс CBV - для редактирования сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "message/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDeleteView(EmailVerifiedMixin, LoginRequiredMixin, DeleteView):
    """Класс CBV - для удаления сообщения."""

    model = Message
    template_name = "message/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            form.add_error(None, "Нельзя удалить сообщение: оно используется в рассылках.")
        return self.form_invalid(form)


# ----------------------- CRUD Mailing ------------------------------


class MailingListView(EmailVerifiedMixin, LoginRequiredMixin, ListView):
    """Класс CBV - выводит список рассылок"""

    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 30
    ordering = ("-start_datetime",)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return queryset

        return super().get_queryset().filter(owner=self.request.user)


class MailingDetailView(EmailVerifiedMixin, LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_details_view.html"
    context_object_name = "mailing"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return queryset

        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(EmailVerifiedMixin, LoginRequiredMixin, CreateView):
    """Класс CBV - для создания рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(EmailVerifiedMixin, LoginRequiredMixin, UpdateView):
    """Класс CBV - для редактирования рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class MailingDeleteView(EmailVerifiedMixin, LoginRequiredMixin, DeleteView):
    """Класс CBV - для удаления рассылки"""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class MailingSendView(EmailVerifiedMixin, LoginRequiredMixin, View):

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.owner == self.request.user:
            mailing.update_status()
            return render(
            request, template_name="mailing/mailing_confirm_send.html", context={"pk": pk, "object": mailing}
            )
        else:
            return HttpResponseForbidden ("Нет прав доступа")

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.owner != self.request.user:
            return HttpResponseForbidden ("Нет прав доступа")

        # логика отправки писем
        try:
            result = send_email(mailing)
        except forms.ValidationError as e:
            return render(
                request,
                template_name="mailing/mailing_confirm_send.html",
                context={"pk": pk, "object": mailing, "errors": e.messages},
            )

        messages.info(
            request,
            f"Отправка завершена. "
            f"Успешно: {result['success_attempts']}. "
            f"Неуспешно: {result['failed_attempts']}.",
        )

        return HttpResponseRedirect(reverse("mailing:mailing_detail_view", kwargs={"pk": pk}))

class MailingDisableView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailing.disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_enabled = False
        mailing.save(update_fields=["is_enabled"])

        return HttpResponseRedirect(
            reverse(
                "mailing:mailing_detail_view",
                kwargs={"pk": mailing.pk},
            )
        )

class MailingEnableView(EmailVerifiedMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailing.disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_enabled = True
        mailing.save(update_fields=["is_enabled"])

        return HttpResponseRedirect(
            reverse(
                "mailing:mailing_detail_view",
                kwargs={"pk": mailing.pk},
            )
        )
