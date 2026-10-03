from django import forms

from .models import Recipient


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