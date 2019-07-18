from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import viewsets, status

from .models import Message, MessageSerializer, Measurement, MeasurementSerializer, Device, DeviceSerializer


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


import datetime
import random
def generate_data(request):
    for d in range(1, 32):
        for h in range(0, 24):
            date = datetime.datetime(2019, 5, d, h, 0, 0)
            m = Measurement(datetime=date, measure_a=random.random(), measure_b=random.random(), measure_c=random.random(), measure_d=random.random())
            m.save()

import json
import numpy as np

@csrf_exempt
def calc_device(request):
    d = json.loads(request.body)

    V_A0 = float(d['V_A0'])
    V_B0 = float(d['V_B0'])
    V_C0 = float(d['V_C0'])
    V_D0 = float(d['V_D0'])

    f_Aa = float(d['f_Aa'])
    f_Ab = float(d['f_Ab'])
    f_Ba = float(d['f_Ba'])
    f_Bb = float(d['f_Bb'])
    f_Ca = float(d['f_Ca'])
    f_Cb = float(d['f_Cb'])
    f_Da = float(d['f_Da'])
    f_Db = float(d['f_Db'])

    f_A = f_Aa * V_A0 + f_Ab
    f_B = f_Ba * V_B0 + f_Bb
    f_C = f_Ca * V_C0 + f_Cb
    f_D = f_Da * V_D0 + f_Db

    L_Ak = float(d['L_Ak'])
    L_Bk = float(d['L_Bk'])
    L_Ck = float(d['L_Ck'])
    L_Dk = float(d['L_Dk'])

    L_A0 = L_Ak + f_A
    L_B0 = L_Bk + f_B
    L_C0 = L_Ck + f_C
    L_D0 = L_Dk + f_D

    D = float(d['D'])
    w1 = float(d['w1'])
    w2 = float(d['w2'])
    dsmall = float(d['dsmall'])

    Q_bar = float(d['Q_bar'])
    G_bar = float(d['G_bar'])
    F_bar = float(d['F_bar'])

    theta_x = float(d['theta_x'])
    theta_y = float(d['theta_y'])
    theta_z = float(d['theta_z'])

    d['M00'] = (D + G_bar) / L_A0
    d['M01'] = (Q_bar) / L_A0
    d['M02'] = (F_bar) / L_A0
    d['M03'] = 0

    d['M10'] = (D + G_bar - w2 * theta_z) / L_B0
    d['M11'] = (w2 - w1 + Q_bar) / L_B0
    d['M12'] = (F_bar + w2 * theta_x) / L_B0
    d['M13'] = ((D + G_bar) * w2 * theta_x + F_bar * w2 * theta_z) / L_B0

    d['M20'] = (D + G_bar - w2 * theta_y) / L_C0
    d['M21'] = (w2 * theta_x + Q_bar) / L_C0
    d['M22'] = (w1 - w2 + F_bar) / L_C0
    d['M23'] = (-(D + G_bar) * w2 + w2 * theta_y * (F_bar + w1)) / L_C0
    
    d['M30'] = (D - dsmall * theta_z - dsmall * theta_y + G_bar) / L_D0
    d['M31'] = (-0.5 * w1 + Q_bar + dsmall * theta_x + dsmall) / L_D0
    d['M32'] = (-0.5 * w1 + F_bar + dsmall * theta_x - dsmall) / L_D0
    d['M33'] = ((D + G_bar) * dsmall * (theta_x - 1) + (theta_z + theta_y) * dsmall * (F_bar + 0.5 * w2)) / L_D0

    coef = np.array([
        [d['M00'], d['M01'], d['M02'], d['M03']],
        [d['M10'], d['M11'], d['M12'], d['M13']],
        [d['M20'], d['M21'], d['M22'], d['M23']],
        [d['M30'], d['M31'], d['M32'], d['M33']],
    ])

    coef_inv = np.linalg.inv(coef)

    d['inv00'] = coef_inv[0][0]
    d['inv01'] = coef_inv[0][1]
    d['inv02'] = coef_inv[0][2]
    d['inv03'] = coef_inv[0][3]

    d['inv10'] = coef_inv[1][0]
    d['inv11'] = coef_inv[1][1]
    d['inv12'] = coef_inv[1][2]
    d['inv13'] = coef_inv[1][3]

    d['inv20'] = coef_inv[2][0]
    d['inv21'] = coef_inv[2][1]
    d['inv22'] = coef_inv[2][2]
    d['inv23'] = coef_inv[2][3]

    d['inv30'] = coef_inv[3][0]
    d['inv31'] = coef_inv[3][1]
    d['inv32'] = coef_inv[3][2]
    d['inv33'] = coef_inv[3][3]

    print(d)

    device = Device.objects.filter(id=d['id'])
    device.update(**d)

    return JsonResponse({}, safe=False, status=status.HTTP_200_OK)