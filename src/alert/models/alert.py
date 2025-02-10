from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User
from celery import current_app

from alert import processors


class AlertProcessor(models.Model):

    TELEGRAM = "TELEGRAM"
    MATTERMOST = "MATTERMOST"
    EMAIL = "EMAIL"
    VIBER = "VIBER"
    WHATSAPP = "WHATSAPP"
    SLACK = "SLACK"

    TYPE_CHOICES = [
        (TELEGRAM, "Telegram"),
        (MATTERMOST, "Mattermost"),
        (EMAIL, "Email"),
        (VIBER, "Viber"),
        (WHATSAPP, "WhatsApp"),
        (SLACK, "Slack"),
    ]

    name = models.CharField(max_length=20, unique=True)
    config = models.JSONField()
    processor_type = models.CharField(max_length=25, choices=TYPE_CHOICES)

    def send_alert(self, alert_config_pk, target, check_id):
        try:
            result = current_app.send_task(
                "alert.tasks.send_alert_task", args=(alert_config_pk, self.id, target, check_id)
            )
        except:
            result = False
        return result

    def __str__(self) -> str:
        return f"{self.processor_type} - {self.name}"

    @property
    def processor(self):
        match self.processor_type:
            case self.TELEGRAM:
                return processors.TelegramProcessor(**self.config)
            case self.MATTERMOST:
                return processors.MattermostProcessor(**self.config)
            case self.EMAIL:
                return processors.EmailProcessor(**self.config)
            case self.VIBER:
                return processors.ViberProcessor(**self.config)
            case self.WHATSAPP:
                return processors.WhatsAppProcessor(**self.config)
            case self.SLACK:
                return processors.SlackProcessor(**self.config)
        return


class AlertConfig(models.Model):
    name = models.CharField(max_length=20, unique=True)
    processor = models.ForeignKey(AlertProcessor, on_delete=models.CASCADE)
    alert_target = models.CharField(max_length=20)
    alert_pause_duration_minutes = models.PositiveIntegerField(default=1)

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.processor}"

    def send_alert(self, check_id):
        if not Alert.objects.filter(
            alert_config=self,
            created_at__gt=timezone.now() - timedelta(minutes=self.alert_pause_duration_minutes),
        ).exists():
            return self.processor.send_alert(self.pk, self.alert_target, check_id)


class Alert(models.Model):
    alert_config = models.ForeignKey(AlertConfig, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    camera_check = models.OneToOneField("cctv.Check", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def short_message(self):
        return self.message[:32]
