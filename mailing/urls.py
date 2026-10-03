from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeTemplateView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, RecipientListView

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeTemplateView.as_view(), name="home"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_add"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
