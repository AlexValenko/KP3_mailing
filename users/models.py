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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
