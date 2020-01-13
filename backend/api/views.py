from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import viewsets, status, filters
from rest_framework.renderers import JSONRenderer

from .models import Measurement, Device
from .serializers import *

from django.db.models.functions import TruncDate
from django.db.models import Min, Max, F

import datetime
import random
import json
import numpy as np

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


def measurement_fill_diff(request):
    measurements = Measurement.objects.filter(diff_a__isnull=True)

    for m in measurements:
        m.save()

    return JsonResponse({'result':'OK'}, safe=False, status=status.HTTP_200_OK)


def measurement_dates(request):
    dates = Measurement.objects

    device_id = request.GET.get('device_id', None)
    if device_id is not None:
        dates = dates.filter(device_id=device_id)

    dates = dates.values('datetime')
    distinct_dates = {d['datetime'].date() for d in dates}
    distinct_dates = sorted(list(distinct_dates))
    return JsonResponse(distinct_dates, safe=False, status=status.HTTP_200_OK)


def measurement_recent(request):
    device_id = request.GET.get('device_id', None)
    last_time = request.GET.get('last_time', None)

    if device_id == None:
        return HttpResponseBadRequest("message: need device_id parameter")

    if last_time == None:
        return HttpResponseBadRequest("message: need last_time parameter")

    last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')

    data = Measurement.objects.filter(device_id=device_id, datetime__gt=last_time).order_by('datetime').all()

    serializer = MeasurementSerializer(data, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


def measurement_aggr(request):
    device_id = request.GET.get('device_id', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if device_id is None:
        return HttpResponseBadRequest("message: need 'device_id' parameter")

    if start_date is None or end_date is None:
        return HttpResponseBadRequest("message: need 'start_date' and 'end_date' parameter")

    year, month, day = start_date.split('-')
    start = datetime.date(int(year), int(month), int(day))

    year, month, day = end_date.split('-')
    end = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=1)

    queryset = Measurement.objects.filter(device_id=device_id, datetime__range=(start, end))
    result = queryset.annotate(date=TruncDate('datetime')).values('date').annotate(
        min_x = Min('diff_x'), max_x = Max('diff_x'),
        min_y = Min('diff_y'), max_y = Max('diff_y'),
        min_z = Min('diff_z'), max_z = Max('diff_z'),
        min_a = Min('diff_a'), max_a = Max('diff_a'),
    ).annotate(
            diff_x=F('max_x') - F('min_x'),
            diff_y=F('max_y') - F('min_y'),
            diff_z=F('max_z') - F('min_z'),
            diff_a=F('max_a') - F('min_a'),
    ).order_by('date')

    result = list(result)
    for r in result:
        r['date'] = r['date'].strftime("%Y-%m-%d")

    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)


def generate_data(request):
    Measurement.objects.all().delete()

    for d in range(1, 5):
        for h in range(0, 24):
            for minute in range(0, 59):
                date = datetime.datetime(2019, 5, d, h, minute, 0)
                m = Measurement(datetime=date, measure_a=random.random(), measure_b=random.random(), measure_c=random.random(), measure_d=random.random())
                m.save()


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

    device = Device.objects.filter(id=d['id'])
    device.update(**d)

    return JsonResponse({}, safe=False, status=status.HTTP_200_OK)


def tmp(request):
    start_time = datetime.datetime(2020, 1, 9, 9, 44)
    end_time = datetime.datetime(2020, 1, 13, 23, 29)
    count = 0
    for data in Measurement.objects.filter(device_id='b8:27:eb:07:06:58', datetime__gt=start_time, datetime__lt=end_time).order_by('datetime').all():
        data.save()
        count += 1

    return JsonResponse({'count': count}, safe=False, status=status.HTTP_200_OK)
