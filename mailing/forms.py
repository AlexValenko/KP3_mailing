from django import forms

from .models import Recipient, Message


class RecipientForm(forms.ModelForm):
    """Класс для описания формы получателей рассылки"""
    class Meta:
        model = Recipient
        fields = ("email", "full_name", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "example@mail.com",
            }
        )

        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Иванов Иван Иванович",
            }
        )

        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Комментарий о получателе",
                "rows": 4,
            }
        )

        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"

class MessageForm(forms.ModelForm):
    """Форма для создания и редактирования сообщений"""

    class Meta:
        model = Message
        fields = ("subject", "body")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Тема письма",
            }
        )

        self.fields["body"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Текст письма",
                "rows": 8,
            }
        )