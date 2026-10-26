from smtplib import SMTPException

from django.core.mail import send_mail
from django.forms import forms
from django.utils import timezone

from mailing.models import MailingAttempt


def send_email(mailing):
    """Функция для отправки писем"""
    start_datetime = mailing.start_datetime
    end_datetime = mailing.end_datetime
    now = timezone.now()

    if not start_datetime <= now <= end_datetime:
        raise forms.ValidationError("Отправка недоступна: текущее время вне периода рассылки.")

    recipients = mailing.recipients.all()

    if not recipients:
        raise forms.ValidationError("Рассылка не содержит получателей")

    attempts_list = []
    success_attempts = 0
    failed_attempts = 0

    for recipient in recipients:
        subject = mailing.message.subject
        message = mailing.message.body
        from_email = "my_mail@mail.ru"
        recipients_list = [
            recipient.email,
        ]
        try:
            result_send = send_mail(
                subject=subject, message=message, from_email=from_email, recipient_list=recipients_list
            )

            if result_send == 1:
                status = "success"
                server_response = f"Получатель: {recipient.email}. " "Почтовый backend сообщил об успешной отправке."
            else:
                status = "failed"
                server_response = f"Получатель: {recipient.email}. " "Почтовый backend вернул 0: письмо не отправлено."
        except SMTPException as e:
            status = "failed"
            server_response = f"Получатель: {recipient.email}. Ошибка: {e}"

        except OSError as e:
            status = "failed"
            server_response = f"Получатель: {recipient.email}. Ошибка: {e}"

        if status == "success":
            success_attempts += 1
        else:
            failed_attempts += 1

        attempt = MailingAttempt(status=status, server_response=server_response, mailing=mailing)
        attempts_list.append(attempt)

    MailingAttempt.objects.bulk_create(attempts_list)

    return {
        "success_attempts": success_attempts,
        "failed_attempts": failed_attempts,
    }
