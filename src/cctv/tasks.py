import logging
from datetime import timedelta
from io import BytesIO

import cv2
from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image

from .models import Camera, Check, CheckConfig
from .utils.analyzer import SimpleImageAnalazer

logger = logging.getLogger("celery")



@shared_task
def check_camera_connection(camera_id) -> None:
    tries_number = 3
    n_checks = 3
    multiple_warnings_statuses = ['WARNING_MULTIPLE', 'WARNING']
    camera = Camera.objects.get(id=camera_id)
    camera_check_config, _ = CheckConfig.objects.get_or_create(
        camera=camera, defaults=dict(saving_image_interval=1,),
    )
    status = Check.UNKNOWN
    image_io = BytesIO()
    # Simulate an RTSP connection check by pinging the camera
    for i in range(tries_number):
        try:
            cap = cv2.VideoCapture(camera.ip_address, cv2.CAP_FFMPEG)

            if cap.isOpened():
                _, frame_bgr = cap.read()
                cap.release()

                frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                result = SimpleImageAnalazer.analyse_image(frame)

                if result == 0:
                    status = Check.OK
                elif result == 1:
                    status = Check.WARNING
                    if i != (tries_number - 1):
                        continue
                else:
                    status = Check.WARNING_ARTIFACTS
                    if i != (tries_number - 1):
                        continue

                last_n_checks = Check.objects.filter(camera=camera).order_by(
                    "-created_at"
                )[:n_checks]
                last_n_checks_status = [check.status for check in last_n_checks]
                if all(status in multiple_warnings_statuses for status in last_n_checks_status)\
                        and status != Check.OK:
                    status = Check.WARNING_MULTIPLE

                # Save by the interval
                last_checks = Check.objects.filter(camera=camera).order_by(
                    "-created_at"
                )[: (camera_check_config.saving_image_interval - 1)]
                if not any([el.image for el in last_checks]):
                    image = Image.fromarray(frame)
                    image.save(image_io, format="JPEG")
                break
            else:
                status = Check.OFFLINE
        except Exception as e:
            status = Check.ERROR
            logger.error(
                f"Camera: {camera.ip_address_safe} | Error while checking: {e}",
                exc_info=True,
            )

        if ttl := camera_check_config.image_ttl:
            checks = (
                Check.objects.filter(
                    camera=camera,
                    created_at__lt=timezone.now() - timedelta(**{ttl.period: ttl.number}),
                )
                .exclude(image__isnull=True, image="")
                .all()
            )
            for check in checks:
                logger.info(
                    f"Camera: {camera.ip_address_safe} | Image was deleted: {check.image}"
                )
                check.image.delete()
                check.image = None
                check.save()

    check = Check.objects.create(
        camera=camera, created_at=timezone.now(), status=status
    )

    if content := image_io.getvalue():
        image_file = ContentFile(content, "file.jpg")
        check.image.save(
            f"{camera.ip_address_safe} - {check.created_at}.jpg", image_file
        )

    # check.save()
    logger.info(f"Camera: {camera.ip_address_safe} | Checked: {status}")
    # Send Alert if status isn't OK
    if status != Check.OK:
        for alert_config in camera.alert_configs.filter(enabled=True).all():
            alert_config.send_alert(check.pk)
