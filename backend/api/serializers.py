from rest_framework import serializers

from .models import Measurement, Device

__all__ = [
    'MeasurementSerializer',
    'DeviceSerializer',
]


class MeasurementSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Measurement
        fields = ('device_id', 'datetime', 'measure_a', 'measure_b',
                  'measure_c', 'measure_d', 'diff_x', 'diff_y', 'diff_z', 'diff_a')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'device_id', 'device_type', 'params')
