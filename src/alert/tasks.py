from datetime import timedelta
import logging

from celery import shared_task
from django.utils import timezone

from .models import Alert, AlertProcessor, AlertConfig
from cctv.models import Check

logger = logging.getLogger("celery")


@shared_task
def send_alert_task(alert_config_pk, processor_id, target, check_id):
    alert_processor = AlertProcessor.objects.get(pk=processor_id)
    check = Check.objects.get(pk=check_id)
    logger.error(f"{alert_processor.name} =- AAAAAAAAAAAAAAAA")
    message = (
        f"Alert Status: {check.status}\n"
        f"Time: {check.created_at}\n"
        f"Camera: {check.camera.ip_address_safe}"
    )
    result = alert_processor.processor.send_alert(target, message)
    alert = Alert.objects.create(
        alert_config_id=alert_config_pk, message=message, camera_check=check
    )
