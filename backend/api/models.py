import numpy as np
import math
import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
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

        F_a = device.params['F_a']
        F_b = device.params['F_b']
        L_k = device.params['L_k']
        V_0 = device.params['V_0']

        F = np.multiply(F_a, V) + F_b
        L = F + L_k

        F_0 = np.multiply(F_a, V_0) + F_b
        L_0 = F_0 + L_k

        delta = L - L_0

        x, y, z, a = np.matmul(device.params['inv_matrix'], delta)
        a = a * 180 / math.pi  # convert rad to deg

        return (x, y, z, a)

    def diff_adv_v3(self, device):
        delta = [self.measure_a, self.measure_b, self.measure_c, self.measure_d]

        x, y, z, a = np.matmul(device.params['inv_matrix'], delta)
        a = a * 180 / math.pi  # convert rad to deg

        return (x, y, z, a)

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


class Device(models.Model):
    name = models.CharField(max_length=20)  # same as device_id
    device_id = models.CharField(max_length=17)
    device_type = models.CharField(max_length=17, default="default")

    params = JSONField(default=dict)

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

    x_min = models.FloatField(default=-10.0)
    y_min = models.FloatField(default=-10.0)
    z_min = models.FloatField(default=-10.0)
    t_min = models.FloatField(default=-10.0)

    x_max = models.FloatField(default=10.0)
    y_max = models.FloatField(default=10.0)
    z_max = models.FloatField(default=10.0)
    t_max = models.FloatField(default=10.0)

    def __str__(self):
        return f"{self.name} ({self.device_id}) - {self.device_type}"
