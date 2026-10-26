from django import forms
from django.utils import timezone

from .models import Mailing, Message, Recipient


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


class MailingForm(forms.ModelForm):
    """Форма для создания и редактирования рассылок"""

    class Meta:
        model = Mailing
        fields = (
            "start_datetime",
            "end_datetime",
            # "status",
            "message",
            "recipients",
        )

        widgets = {
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            # Поле заполняется автоматически по датам
            # "status": forms.Select(
            #     attrs={
            #         "class": "form-select",
            #     }
            # ),
            "message": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "recipients": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": 8,
                }
            ),
        }

        labels = {
            "start_datetime": "Дата и время первой отправки",
            "end_datetime": "Дата и время окончания отправки",
            # "status": "Статус",
            "message": "Сообщение",
            "recipients": "Получатели",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_datetime"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]
        self.fields["end_datetime"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]

    def clean_start_datetime(self):
        """Проверяет, что start_time не может быть в прошлом."""
        start_datetime = self.cleaned_data.get("start_datetime")
        now = timezone.now()

        is_new = self.instance.pk is None
        start_changed = "start_datetime" in self.changed_data

        if is_new or start_changed:
            if not start_datetime or start_datetime <= now:
                raise forms.ValidationError("Дата начала не может быть в прошлом")
        return start_datetime

    def clean(self):
        """Проверяет корректность периода рассылки."""
        cleaned_data = super().clean()

        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")

        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise forms.ValidationError("Дата окончания должна быть позже даты первой отправки")

        return cleaned_data
