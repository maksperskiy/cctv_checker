from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name",)
    fields = ("name", "cameras")
    readonly_fields = ("cameras",)

    def cameras(self, obj):
        return ", ".join([el.ip_address for el in obj.camera_set.all()])
