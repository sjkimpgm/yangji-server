# Generated by Django 2.2.1 on 2019-07-17 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190717_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='dsmall',
            field=models.FloatField(default=0.0),
        ),
    ]