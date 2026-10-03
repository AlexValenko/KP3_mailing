from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Mailing, Recipient

class HomeTemplateView(TemplateView):
    """Класс CBV для отображения домашней страницы - отображает статистику о рассылках и получателях"""
    template_name = "home.html"


