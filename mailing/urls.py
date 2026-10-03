from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeTemplateView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, RecipientListView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeTemplateView.as_view(), name="home"),
    # Получатели
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_add"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(),name="message_add"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]
