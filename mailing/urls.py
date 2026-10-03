from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeTemplateView

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeTemplateView.as_view(), name="home"),
]
