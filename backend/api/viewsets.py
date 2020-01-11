from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *

__all__ = [
    'MeasurementViewSet',
    'DeviceViewSet',
]


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['datetime']
    ordering = ['datetime']

    def get_queryset(self):
        queryset = Measurement.objects.all()
        device_id = self.request.query_params.get('device_id', None)
        target_date = self.request.query_params.get('target_date', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if device_id is not None:
            queryset = queryset.filter(device_id=device_id)

        if target_date is not None:
            year, month, day = target_date.split('-')
            queryset = queryset.filter(datetime__date=datetime.date(int(year), int(month), int(day)))
        elif start_date is not None and end_date is not None:
            year, month, day = start_date.split('-')
            start = datetime.date(int(year), int(month), int(day))

            year, month, day = end_date.split('-')
            end = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=1)

            queryset = queryset.filter(datetime__range=(start, end))

            stride = int(len(queryset) / 1000)
            if stride < 1:
                stride = 1

            # queryset = queryset[::stride]
        return queryset


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['get'])
    def set_params(self, request, pk=None):
        d = self.get_object()
        d.params['matrix'] = [
            [d.M00, d.M01, d.M02, d.M03],
            [d.M10, d.M11, d.M12, d.M13],
            [d.M20, d.M21, d.M22, d.M23],
            [d.M30, d.M31, d.M32, d.M33],
        ]

        d.params['inv_matrix'] = [
            [d.inv00, d.inv01, d.inv02, d.inv03],
            [d.inv10, d.inv11, d.inv12, d.inv13],
            [d.inv20, d.inv21, d.inv22, d.inv23],
            [d.inv30, d.inv31, d.inv32, d.inv33],
        ]

        d.params['limit_min'] = [d.x_min, d.y_min, d.z_min, d.t_min]
        d.params['limit_max'] = [d.x_max, d.y_max, d.z_max, d.t_max]

        if d.device_type == 'default':
            d.params['F_a'] = [d.f_Aa, d.f_Ba, d.f_Ca, d.f_Da]
            d.params['F_b'] = [d.f_Ab, d.f_Bb, d.f_Cb, d.f_Db]
            d.params['L_k'] = [d.L_Ak, d.L_Bk, d.L_Ck, d.L_Dk]
            d.params['V_0'] = [d.V_A0, d.V_B0, d.V_C0, d.V_D0]

        d.save()

        return Response({'status': 'json fields are set'})
