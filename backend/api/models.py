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

    V_A0 = models.FloatField(default=0.0)
    V_B0 = models.FloatField(default=0.0)
    V_C0 = models.FloatField(default=0.0)
    V_D0 = models.FloatField(default=0.0)

    w1 = models.FloatField(default=0.0)
    w2 = models.FloatField(default=0.0)
    D = models.FloatField(default=0.0)
    dsmall = models.FloatField(default=0.0)
    H = models.FloatField(default=0.0)

    G_bar = models.FloatField(default=0.0)
    Q_bar = models.FloatField(default=0.0)
    F_bar = models.FloatField(default=0.0)
    theta_x = models.FloatField(default=0.0)
    theta_y = models.FloatField(default=0.0)
    theta_z = models.FloatField(default=0.0)

    f_Aa = models.FloatField(default=0.0)
    f_Ab = models.FloatField(default=0.0)

    f_Ba = models.FloatField(default=0.0)
    f_Bb = models.FloatField(default=0.0)

    f_Ca = models.FloatField(default=0.0)
    f_Cb = models.FloatField(default=0.0)

    f_Da = models.FloatField(default=0.0)
    f_Db = models.FloatField(default=0.0)

    L_Ak = models.FloatField(default=0.0)
    L_Bk = models.FloatField(default=0.0)
    L_Ck = models.FloatField(default=0.0)
    L_Dk = models.FloatField(default=0.0)

    M00 = models.FloatField(default=0.0)
    M01 = models.FloatField(default=0.0)
    M02 = models.FloatField(default=0.0)
    M03 = models.FloatField(default=0.0)
    M10 = models.FloatField(default=0.0)
    M11 = models.FloatField(default=0.0)
    M12 = models.FloatField(default=0.0)
    M13 = models.FloatField(default=0.0)
    M20 = models.FloatField(default=0.0)
    M21 = models.FloatField(default=0.0)
    M22 = models.FloatField(default=0.0)
    M23 = models.FloatField(default=0.0)
    M30 = models.FloatField(default=0.0)
    M31 = models.FloatField(default=0.0)
    M32 = models.FloatField(default=0.0)
    M33 = models.FloatField(default=0.0)

    inv00 = models.FloatField(default=0.0)
    inv01 = models.FloatField(default=0.0)
    inv02 = models.FloatField(default=0.0)
    inv03 = models.FloatField(default=0.0)
    inv10 = models.FloatField(default=0.0)
    inv11 = models.FloatField(default=0.0)
    inv12 = models.FloatField(default=0.0)
    inv13 = models.FloatField(default=0.0)
    inv20 = models.FloatField(default=0.0)
    inv21 = models.FloatField(default=0.0)
    inv22 = models.FloatField(default=0.0)
    inv23 = models.FloatField(default=0.0)
    inv30 = models.FloatField(default=0.0)
    inv31 = models.FloatField(default=0.0)
    inv32 = models.FloatField(default=0.0)
    inv33 = models.FloatField(default=0.0)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'