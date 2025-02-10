from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import AlertConfig, AlertProcessor, Alert


@admin.register(AlertConfig)
class AlertConfigAdmin(ModelAdmin):
    list_display = ("name", "processor", "alert_target", "enabled")
    fields = ("name", "users", "processor", "alert_target", "alert_pause_duration_minutes", "enabled")
    
    # def has_module_permission(self, request):
    #     return True
    # def has_view_permission(self, request, obj = ...):
    #     return True
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)

    #     # Check the user's role or permissions
    #     if request.user.is_superuser:  # If user is superuser, show all orders
    #         return queryset
    #     elif request.user.groups.filter(name="Managers").exists():  # If user is a manager
    #         return queryset
    #     else:  # If the user is an employee, show only their orders
    #         return queryset.filter(created_by=request.user)


@admin.register(AlertProcessor)
class AlertProcessorAdmin(ModelAdmin):
    list_display = ("name", "processor_type")
    fields = ("name", "processor_type", "config")

    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj = ...):
        return True


@admin.register(Alert)
class AlertAdmin(ModelAdmin):
    list_display = ("alert_config", "created_at", "short_message")
    fields = ("alert_config", "created_at", "message")
    readonly_fields = ("alert_config", "created_at", "message")

    def has_view_permission(self, request, obj = ...):
        return True
    
    def has_module_permission(self, request):
        return True