# Generated by Django 5.1.3 on 2024-12-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_remove_alert_created_at_alert_camera_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
