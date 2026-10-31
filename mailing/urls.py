from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (
    MailingDisableView,
    HomeTemplateView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingSendView,
    MailingUpdateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
    MailingEnableView,
)

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeTemplateView.as_view(), name="home"),
    # Получатели
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_details"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_add"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    # Сообщения
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail_view"),
    path("messages/create/", MessageCreateView.as_view(), name="message_add"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    # Рассылки
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail_view"),
    path("mailings/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_add"),
    path("mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path('mailings/<int:pk>/disable/', MailingDisableView.as_view(), name='mailing_disable'),
    path('mailings/<int:pk>/enable/', MailingEnableView.as_view(), name='mailing_enable'),
]
