from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from users.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class StyleMixin:
    """Общая стилизация полей форм Bootstrap."""

    field_styles = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, placeholder in self.field_styles.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {
                        "class": "form-control",
                        "placeholder": placeholder,
                    }
                )


class CustomUserCreationForm(StyleMixin, UserCreationForm):
    """Форма регистрации пользователя."""

    field_styles = {
        "email": "Введите Email (обязательное поле)",
        "phone_number": "Введите номер телефона (необязательно)",
        "avatar": "Загрузите изображение (необязательно)",
        "first_name": "Введите ваше имя (необязательно)",
        "last_name": "Введите вашу фамилию (необязательно)",
        "password1": "Введите пароль",
        "password2": "Повторите пароль",
    }

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "phone_number",
            "avatar",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class CustomAuthenticationForm(StyleMixin, AuthenticationForm):
    """Форма авторизации пользователя."""

    field_styles = {
        "username": "Введите Email",
        "password": "Введите пароль",
    }


class CustomUserUpdateForm(StyleMixin, ModelForm):
    """Форма редактирования профиля пользователя."""

    field_styles = {
        "email": "Введите Email",
        "phone_number": "Введите номер телефона",
        "avatar": "Загрузите изображение",
        "user_country": "Введите название страны",
        "first_name": "Введите имя",
        "last_name": "Введите фамилию",
    }

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
        )

        labels = {
            "email": "Email",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "avatar": "Аватар",
        }

class CustomUserUpdatePassForm(StyleMixin, PasswordChangeForm):
    field_styles = {
        "old_password": "Введите старый пароль",
        "new_password1": "Введите новый пароль",
        "new_password2": "Повторите новый пароль",
    }