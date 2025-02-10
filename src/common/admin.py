from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from unfold.admin import ModelAdmin, UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass



from django.contrib import admin
from django import forms

from .models import S3Config


class S3ConfigForm(forms.ModelForm):
    access_key = forms.CharField(required=False, widget=UnfoldAdminTextInputWidget)
    secret_key = forms.CharField(required=False, widget=UnfoldAdminTextInputWidget)

    class Meta:
        model = S3Config
        fields = ['url', 'bucket_name', 'region_name', 'access_key', 'secret_key']

    def __init__(self, *args, **kwargs):
        """Override the init method to store the original encrypted values."""
        super(S3ConfigForm, self).__init__(*args, **kwargs)
        
        # Store the original values for comparison
        if self.instance and self.instance.pk:
            # Load decrypted values into form for display if instance exists
            self.fields['access_key'].initial = ''  # Leave access key and secret key empty
            self.fields['secret_key'].initial = ''  # Don't display these values
        else:
            # New instance, no initial values
            self.fields['access_key'].initial = None
            self.fields['secret_key'].initial = None

    def save(self, commit=True):
        """Override save method to encrypt access_key and secret_key only if they have changed."""
        instance = super(S3ConfigForm, self).save(commit=False)

        # Encrypt the access_key only if a new value is provided
        if self.cleaned_data['access_key']:
            # Check if it's a new instance or if the access_key has changed
            if not instance.encrypted_access_key or self.cleaned_data['access_key']:
                instance.encrypted_access_key = S3Config._encrypt(self.cleaned_data['access_key'])

        # Encrypt the secret_key only if a new value is provided
        if self.cleaned_data['secret_key']:
            # Check if it's a new instance or if the secret_key has changed
            if not instance.encrypted_secret_key or self.cleaned_data['secret_key']:
                instance.encrypted_secret_key = S3Config._encrypt(self.cleaned_data['secret_key'])

        if commit:
            instance.save()

        return instance

@admin.register(S3Config)
class S3ConfigAdmin(ModelAdmin):
    form = S3ConfigForm
