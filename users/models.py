from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """Класс описания пользователей сайта"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон",
        region="RU",
        help_text="Введите свой номер телефона (необязательно)",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        null=True,
        blank=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение (необязательно)",
    )
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email подтверждён",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("block_user", "Может блокировать пользователей"),
        ]

    def __str__(self):
        return self.email
