from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    """ORM модель для получателей рассылок"""

    email = models.EmailField(unique=True, verbose_name="Email", help_text="email получателя")
    full_name = models.CharField(max_length=255, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"


class Message(models.Model):
    """ORM модель для писем"""

    subject = models.CharField(max_length=255, verbose_name="Тема письма", help_text="Тема")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """ORM модель для рассылок"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, related_name="mailings", verbose_name="Получатели")

    def __str__(self):
        return f"Рассылка #{self.pk} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def update_status(self):
        now = timezone.now()
        if now < self.start_datetime:
            actual_status = "created"
        elif self.start_datetime <= now <= self.end_datetime:
            actual_status = "started"
        else:
            actual_status = "completed"

        if self.status != actual_status:
            self.status = actual_status
            self.save()


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус попытки")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts", verbose_name="Рассылка")

    def __str__(self):
        return f"Попытка рассылки #{self.mailing_id} — " f"{self.get_status_display()}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
