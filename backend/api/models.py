from django.db import models
from rest_framework import serializers


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')


# FIXME(sjkim): assume single device
class Measurement(models.Model):
    datetime = models.DateTimeField()

    measure_a = models.FloatField()
    measure_b = models.FloatField()
    measure_c = models.FloatField()
    measure_d = models.FloatField()

    def __str__(self):
        return "{}: {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(self.datetime.strftime("%Y-%m-%d %H:%M:%S"), self.measure_a, self.measure_b, self.measure_c, self.measure_d)


class MeasurementSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Measurement
        fields = ('datetime', 'measure_a', 'measure_b', 'measure_c', 'measure_d')


class Device(models.Model):
    name = models.CharField(max_length=20)

    w1 = models.FloatField()
    w2 = models.FloatField()
    d1 = models.FloatField()
    d2 = models.FloatField()
    H = models.FloatField()
    D = models.FloatField()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'w1', 'w2', 'd1', 'd2', 'H', 'D')