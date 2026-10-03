from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .models import Recipient

from .forms import RecipientForm

class HomeTemplateView(TemplateView):
    """Класс CBV для отображения домашней страницы - отображает статистику о рассылках и получателях"""
    template_name = "home.html"


    # ----------------------- CRUD Recipient ------------------------------
class RecipientListView(ListView):
    """Класс CBV для вывода списка получателей рассылки"""

    model = Recipient
    template_name = "recipient_list.html"
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


class RecipientCreateView(CreateView):
    """Класс CBV для создания получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientUpdateView(UpdateView):
    """Класс CBV для редактирования получателя."""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientDeleteView(DeleteView):
    """Класс CBV для удаления получателя."""

    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")
