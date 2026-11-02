from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создает суперпользователя. Почта не требует верификации"""
        user = CustomUser.objects.create(email="admin@admin.com")
        user.set_password("Admin_Pass_1234")
        user.is_active = True
        user.email_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
