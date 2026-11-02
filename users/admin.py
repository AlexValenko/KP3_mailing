from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    exclude = (
        "password",
        "is_superuser",
    )
    search_fields = ("email",)
    ordering = ("-date_joined",)
