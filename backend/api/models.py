from django.db import models
from rest_framework import serializers
import math

from django.dispatch import receiver
from django.db.models.signals import pre_save


class Measurement(models.Model):
    device_id = models.CharField(max_length=17)
    datetime = models.DateTimeField()

    measure_a = models.FloatField()
    measure_b = models.FloatField()
    measure_c = models.FloatField()
    measure_d = models.FloatField()

    diff_x = models.FloatField(null=True, blank=True)
    diff_y = models.FloatField(null=True, blank=True)
    diff_z = models.FloatField(null=True, blank=True)
    diff_a = models.FloatField(null=True, blank=True)

    def diff(self):
        device = Device.objects.filter(device_id=self.device_id)[0]

        if device.device_type == "default":
            return self.diff_default(device)
        elif device.device_type == "adv_v3":
            return self.diff_adv_v3(device)

    def diff_default(self, device):
        V = [self.measure_a, self.measure_b, self.measure_c, self.measure_d]

        F_a = [device.f_Aa, device.f_Ba, device.f_Ca, device.f_Da]
        F_b = [device.f_Ab, device.f_Bb, device.f_Cb, device.f_Db]

        F = [F_a[i] * V[i] + F_b[i] for i in range(4)]

        Lk = [device.L_Ak, device.L_Bk, device.L_Ck, device.L_Dk]
        L = [F[i] + Lk[i] for i in range(4)]

        V_0 = [device.V_A0, device.V_B0, device.V_C0, device.V_D0]

        F_0 = [F_a[i] * V_0[i] + F_b[i] for i in range(4)]
        L_0 = [F_0[i] + Lk[i] for i in range(4)]

        delta = [L[i] - L_0[i] for i in range(4)]

        inv_A = [device.inv00, device.inv01, device.inv02, device.inv03]
        inv_B = [device.inv10, device.inv11, device.inv12, device.inv13]
        inv_C = [device.inv20, device.inv21, device.inv22, device.inv23]
        inv_D = [device.inv30, device.inv31, device.inv32, device.inv33]

        x = [delta[i] * inv_A[i] for i in range(4)]
        y = [delta[i] * inv_B[i] for i in range(4)]
        z = [delta[i] * inv_C[i] for i in range(4)]
        a = [delta[i] * inv_D[i] for i in range(4)]

        return (sum(x), sum(y), sum(z), sum(a) * 180 / math.pi)

    def diff_adv_v3(self, device):
        delta = [self.measure_a, self.measure_b, self.measure_c, self.measure_d]

        inv_A = [device.inv00, device.inv01, device.inv02, device.inv03]
        inv_B = [device.inv10, device.inv11, device.inv12, device.inv13]
        inv_C = [device.inv20, device.inv21, device.inv22, device.inv23]
        inv_D = [device.inv30, device.inv31, device.inv32, device.inv33]

        x = [delta[i] * inv_A[i] for i in range(4)]
        y = [delta[i] * inv_B[i] for i in range(4)]
        z = [delta[i] * inv_C[i] for i in range(4)]
        a = [delta[i] * inv_D[i] for i in range(4)]

        return (sum(x), sum(y), sum(z), sum(a) * 180 / math.pi)
        
    def __str__(self):
        x = self.diff_x if self.diff_x else 0
        y = self.diff_y if self.diff_y else 0
        z = self.diff_z if self.diff_z else 0
        a = self.diff_a if self.diff_a else 0

        return "[{}] {}: {:.3f}, {:.3f}, {:.3f}, {:.3f} / {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(self.device_id, self.datetime.strftime("%Y-%m-%d %H:%M:%S"), self.measure_a, self.measure_b, self.measure_c, self.measure_d, x, y, z, a)

@receiver(pre_save, sender=Measurement)
def measurement_pre_save_callback(sender, **kwargs):
    data = kwargs['instance']
    x, y, z, a = data.diff()
    data.diff_x = x
    data.diff_y = y
    data.diff_z = z
    data.diff_a = a

class MeasurementSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Measurement
        fields = ('device_id', 'datetime', 'measure_a', 'measure_b', 'measure_c', 'measure_d', 'diff_x', 'diff_y', 'diff_z', 'diff_a')


class Device(models.Model):
    name = models.CharField(max_length=20) # same as device_id
    device_id = models.CharField(max_length=17)
    device_type = models.CharField(max_length=17, default="default")

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
        fields = ('name', 'device_id')