# Generated by Django 3.0.2 on 2020-01-11 09:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200111_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='latest_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
