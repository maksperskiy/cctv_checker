from django.db import models
from django_celery_beat.models import IntervalSchedule
from django.contrib.auth.models import Group, User

from cctv.utils.common import remove_credentials

from .periodic_task import CheckPeriodicTask
from .tag import Tag
from alert.models.alert import AlertConfig


class Camera(models.Model):
    ip_address = models.CharField(max_length=100, unique=True)
    ip_address_safe = models.CharField(max_length=100, default="")
    tags = models.ManyToManyField(Tag)
    alert_configs = models.ManyToManyField(AlertConfig)

    user_group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.ip_address_safe

    def save(self, *args, **kwargs):
        self.ip_address_safe = remove_credentials(self.ip_address)
        super().save(*args, **kwargs)

        interval, _ = IntervalSchedule.objects.get_or_create(
            every=5, period=IntervalSchedule.MINUTES
        )
        task = CheckPeriodicTask.objects.get_or_create(
            camera=self,
            defaults=dict(
                name=f"task_for_{self.id}",
                task="cctv.tasks.check_camera_connection",
                args=f"[{self.id}]",
                interval=interval,
            ),
        )
