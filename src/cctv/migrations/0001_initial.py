# Generated by Django 5.1.3 on 2024-11-25 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100, unique=True)),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='Unknown', max_length=20)),
            ],
        ),
    ]
