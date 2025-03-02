from django.db import models
from django.core.validators import MinValueValidator

from .camera import Camera


class Check(models.Model):
    OK = "OK"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARNING_MULTIPLE = "WARNING_MULTIPLE"
    UNKNOWN = "UNKNOWN"
    WARNING_ARTIFACTS = "WARNING_ARTIFACTS"

    STATUS_CHOICES = [
        (OK, "Ok"),
        (OFFLINE, "Offline"),
        (ERROR, "Error"),
        (WARNING, "Warning"),
        (UNKNOWN, "Unknown"),
        (WARNING_MULTIPLE, "Multiple warnings"),
        (WARNING_ARTIFACTS, "Artifacts warning")
    ]

    created_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default=UNKNOWN, choices=STATUS_CHOICES)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="checks", null=True, blank=True)

    def __str__(self):
        return f"{self.camera} - {self.created_at}"


DAYS = "days"
HOURS = "hours"
MINUTES = "minutes"
SECONDS = "seconds"
MICROSECONDS = "microseconds"

PERIOD_CHOICES = (
    (DAYS, "Days"),
    (HOURS, "Hours"),
    (MINUTES, "Minutes"),
    (SECONDS, "Seconds"),
    (MICROSECONDS, "Microseconds"),
)

SINGULAR_PERIODS = (
    (DAYS, "Day"),
    (HOURS, "Hour"),
    (MINUTES, "Minute"),
    (SECONDS, "Second"),
    (MICROSECONDS, "Microsecond"),
)


class Duration(models.Model):
    DAYS = DAYS
    HOURS = HOURS
    MINUTES = MINUTES
    SECONDS = SECONDS
    MICROSECONDS = MICROSECONDS

    PERIOD_CHOICES = PERIOD_CHOICES

    number = models.PositiveIntegerField(
        null=False,
        verbose_name="Number of Periods",
        help_text="Number of periods to wait before " "delete the image again",
    )
    period = models.CharField(
        max_length=24,
        choices=PERIOD_CHOICES,
        verbose_name="Duration Period",
        help_text="The type of period between task runs (Example: days)",
    )

    class Meta:
        """Table information."""

        verbose_name = "duration"
        verbose_name_plural = "durations"
        ordering = ["period", "number"]

    def __str__(self):
        readable_period = None
        if self.number == 1:
            for period, _readable_period in SINGULAR_PERIODS:
                if period == self.period:
                    readable_period = _readable_period.lower()
                    break
            return "1 {}".format(readable_period)
        for period, _readable_period in PERIOD_CHOICES:
            if period == self.period:
                readable_period = _readable_period.lower()
                break
        return "{} {}".format(self.number, readable_period)

    @property
    def period_singular(self):
        return self.period[:-1]


class CheckConfig(models.Model):
    camera = models.OneToOneField(
        "cctv.Camera", on_delete=models.CASCADE, null=True, blank=True
    )

    saving_image_interval = models.PositiveIntegerField(default=1)
    image_ttl = models.ForeignKey(
        Duration,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Image Time To Live",
        help_text="Image Time To Live. "
        "Images older than this interval will be deleted from storage.",
    )
    storage = models.ForeignKey(
        "common.S3Config",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Storage",
        help_text="Storage to store images.",
    )

    def __str__(self):
        return str(self.camera)
