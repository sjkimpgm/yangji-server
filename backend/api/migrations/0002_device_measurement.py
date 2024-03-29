# Generated by Django 2.2.1 on 2019-05-21 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('w1', models.FloatField()),
                ('w2', models.FloatField()),
                ('d1', models.FloatField()),
                ('d2', models.FloatField()),
                ('H', models.FloatField()),
                ('D', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('measure_a', models.FloatField()),
                ('measure_b', models.FloatField()),
                ('measure_c', models.FloatField()),
                ('measure_d', models.FloatField()),
            ],
        ),
    ]
