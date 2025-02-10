from django.db import models


class CameraCoordinates(models.Model):
    camera = models.OneToOneField(
        "cctv.Camera", on_delete=models.CASCADE, null=True, blank=True
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
