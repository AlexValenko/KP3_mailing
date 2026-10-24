from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Message, Recipient


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


class RecipientDetailView(DeleteView):
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


# ----------------------- CRUD Mailing ------------------------------


class MailingListView(ListView):
    """Класс CBV - выводит список рассылок."""

    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 30
    ordering = ("-start_datetime",)


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


class MailingDeleteView(DeleteView):
    """Класс CBV - для удаления рассылки"""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
