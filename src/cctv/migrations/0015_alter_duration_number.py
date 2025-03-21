# Generated by Django 5.1.3 on 2024-11-29 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cctv', '0014_duration_alter_checkconfig_image_ttl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration',
            name='number',
            field=models.PositiveIntegerField(help_text='Number of periods to wait before delete the image again', verbose_name='Number of Periods'),
        ),
    ]
