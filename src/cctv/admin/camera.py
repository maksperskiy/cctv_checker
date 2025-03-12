from django import forms
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.import_export.forms import ImportForm

from ..models import (
    Camera,
    Check,
    CheckPeriodicTask,
    CheckConfig,
    Duration,
    CameraCoordinates,
)

# class CameraCheckInline(TabularInline):
#     model = Check
#     tab = True
#     extra = 0
#     # template = 'admin/cameracheck_inline.html'

#     list_display = ("created_at", "status", "image_tag")
#     readonly_fields = ("created_at", "status", "image_tag")

#     def image_tag(self, obj):
#         return format_html(
#             '<img style="height: 240px; aspect-ratio: 16 / 9; object-fit: cover;" src="{}" /><a href="{}">Download</a>'.format(
#                 obj.image.url, obj.image.url
#             )
#         )

#     image_tag.short_description = "Image"

#     ordering = ("-created_at",)


class CameraCheckPeriodicTaskInline(TabularInline):
    model = CheckPeriodicTask
    tab = True
    fields = (
        "interval",
        "crontab",
        "enabled",
    )


class CameraGeolocationInline(TabularInline):
    model = CameraCoordinates
    tab = True
    fields = (
        "latitude",
        "longitude",
    )


@admin.register(Duration)
class DurationAdmin(ModelAdmin):
    pass


class CameraCheckConfigInline(TabularInline):
    model = CheckConfig
    tab = True
    fields = (
        "saving_image_interval",
        "image_ttl",
    )


class CameraTagInline(TabularInline):
    model = Camera.tags.through
    extra = 0
    tab = True
    exclude = ("tags",)


class CameraAlertConfigInline(TabularInline):
    model = Camera.alert_configs.through
    extra = 0
    tab = True
    exclude = ("alert_configs",)


class CameraResource(resources.ModelResource):
    class Meta:
        model = Camera
        # Specify the fields you want to include for import
        fields = "ip_address"  # Replace with your model's fields
        import_id_fields = []


@admin.register(Camera)
class CameraAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = (
        "ip_address_safe",
        "last_status",
        "last_status_flag",
        "last_checked",
    )

    list_filter = ("tags",)

    fields = ("ip_address", "last_status", "last_checked")
    readonly_fields = ("last_status", "last_status_flag", "last_checked")
    inlines = [
        CameraCheckPeriodicTaskInline,
        CameraCheckConfigInline,
        CameraTagInline,
        CameraAlertConfigInline,
        CameraGeolocationInline,
    ]

    resource_class = CameraResource
    import_form_class = ImportForm

    def last_status(self, obj):
        latest_check = Check.objects.filter(camera=obj).order_by("-created_at").first()
        return latest_check.status if latest_check else "No checks"

    def last_checked(self, obj):
        latest_check = Check.objects.filter(camera=obj).order_by("-created_at").first()
        return latest_check.created_at if latest_check else "No checks"

    def last_status_flag(self, obj):
        latest_check = Check.objects.filter(camera=obj).order_by("-created_at").first()

        colors = {
            Check.OK: "#00FF00",
            Check.WARNING: "#FF8C00",
            Check.OFFLINE: "#000000",
            Check.ERROR: "#FF0000",
            Check.UNKNOWN: "#A9A9A9",
            Check.WARNING_MULTIPLE: "#C16C04",
            Check.WARNING_ARTIFACTS: "#A54F0C",
        }
        color = colors[latest_check.status] if latest_check else colors[Check.UNKNOWN]
        return format_html(
            f'<div style="width:24px; height:24px; background:{color};"></div>'
        )

    last_status_flag.short_description = "Image"

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["fields"] = ["ip_address"]
        return super(CameraAdmin, self).get_form(request, obj, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Fetching the Author object
        camera = self.get_object(request, object_id)
        # Adding related books to the context for rendering in the change page
        if extra_context is None:
            extra_context = {}
        extra_context["checks"] = Check.objects.filter(camera=camera).order_by(
            "-created_at"
        )[:500:-1]
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def has_view_permission(self, request, obj=...):
        return request.user.is_superuser or request.user.groups.filter(pk=obj.user_group.pk).exists()

    def save_model(self, request, obj: Camera, form, change):
        if getattr(obj, "user_group", None) is None:
            obj.user_group = request.user.groups.first()
        obj.save()
