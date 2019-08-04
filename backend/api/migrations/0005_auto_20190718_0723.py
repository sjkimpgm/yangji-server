# Generated by Django 2.2.1 on 2019-07-17 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_device_dsmall'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='V_A0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='device',
            name='V_B0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='device',
            name='V_C0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='device',
            name='V_D0',
            field=models.FloatField(default=0.0),
        ),
    ]