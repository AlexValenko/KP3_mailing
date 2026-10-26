from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Message, Recipient
from .services import send_email


class HomeTemplateView(TemplateView):
    """Класс CBV для отображения домашней страницы - отображает статистику о рассылках и получателях"""

    template_name = "home.html"

    # ----------------------- CRUD Recipient ------------------------------


class RecipientListView(ListView):
    """Класс CBV для вывода списка получателей рассылки"""

    model = Recipient
    template_name = "recipient/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 30
    ordering = ("full_name",)

    def get_queryset(self):
        """Возвращает список получателей с учетом поиска."""
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            queryset = queryset.filter(full_name__icontains=search_query)

        return queryset


class RecipientDetailView(DetailView):
    """Класс CBV для просмотра детальной информации о получателе рассылки"""

    model = Recipient
    template_name = "recipient/recipient_detail_view.html"


class RecipientCreateView(CreateView):
    """Класс CBV для создания получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(UpdateView):
    """Класс CBV для редактирования получателя."""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(DeleteView):
    """Класс CBV для удаления получателя."""

    model = Recipient
    template_name = "recipient/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


# ----------------------- CRUD Message ------------------------------


class MessageListView(ListView):
    """Класс CBV - выводит список сообщений"""

    model = Message
    template_name = "message/message_list.html"
    context_object_name = "messages"
    paginate_by = 30
    ordering = ("subject",)

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            queryset = queryset.filter(subject__icontains=search_query)

        return queryset


class MessageDetailView(DetailView):
    """Класс CBV - выводит детали сообщения"""

    model = Message
    template_name = "message/message_detail_view.html"


class MessageCreateView(CreateView):
    """Класс CBV - для создания сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "message/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    """Класс CBV - для редактирования сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "message/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    """Класс CBV - для удаления сообщения."""

    model = Message
    template_name = "message/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            form.add_error(None, "Нельзя удалить сообщение: оно используется в рассылках.")
        return self.form_invalid(form)


# ----------------------- CRUD Mailing ------------------------------


class MailingListView(ListView):
    """Класс CBV - выводит список рассылок."""

    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 30
    ordering = ("-start_datetime",)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_details_view.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class MailingCreateView(CreateView):
    """Класс CBV - для создания рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    """Класс CBV - для редактирования рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class MailingDeleteView(DeleteView):
    """Класс CBV - для удаления рассылки"""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


class MailingSendView(View):

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing
        return render(
            request, template_name="mailing/mailing_confirm_send.html", context={"pk": pk, "object": mailing}
        )

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

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
