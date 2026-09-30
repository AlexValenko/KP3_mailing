from django.contrib import admin

from .models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("email", "full_name", "comment")
    list_filter = ("mailings",)
    ordering = ("full_name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject")
    search_fields = ("subject", "body")
    ordering = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_datetime",
        "end_datetime",
        "status",
        "message",
    )
    list_filter = (
        "status",
        "start_datetime",
        "end_datetime",
    )
    search_fields = (
        "message__subject",
        "message__body",
    )
    filter_horizontal = ("recipients",)
    ordering = ("-start_datetime",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mailing",
        "attempted_at",
        "status",
        "server_response",
    )
    list_filter = (
        "status",
        "attempted_at",
    )
    search_fields = (
        "mailing__message__subject",
        "server_response",
    )
    ordering = ("-attempted_at",)