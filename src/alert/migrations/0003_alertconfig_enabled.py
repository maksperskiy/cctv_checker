# Generated by Django 5.1.3 on 2024-12-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_alter_alertconfig_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertconfig',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
