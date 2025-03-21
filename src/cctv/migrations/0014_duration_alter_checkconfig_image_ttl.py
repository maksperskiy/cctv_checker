# Generated by Django 5.1.3 on 2024-11-29 13:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cctv', '0013_cameracoordinates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(help_text='Number of periods to wait before delete the image again', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Number of Periods')),
                ('period', models.CharField(choices=[('days', 'Days'), ('hours', 'Hours'), ('minutes', 'Minutes'), ('seconds', 'Seconds'), ('microseconds', 'Microseconds')], help_text='The type of period between task runs (Example: days)', max_length=24, verbose_name='Duration Period')),
            ],
            options={
                'verbose_name': 'duration',
                'verbose_name_plural': 'durations',
                'ordering': ['period', 'number'],
            },
        ),
        migrations.AlterField(
            model_name='checkconfig',
            name='image_ttl',
            field=models.ForeignKey(blank=True, help_text='Image Time To Live. Images older than this interval will be deleted from storage.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cctv.duration', verbose_name='Image Time To Live'),
        ),
    ]
