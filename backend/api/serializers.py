from rest_framework import serializers
from django.shortcuts import get_object_or_404

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

    def create(self, validated_data):
        obj = Measurement(**validated_data)
        device = get_object_or_404(Device, device_id=obj.device_id)

        # For default, not apply offset
        if device.device_type == 'default':
            obj.measure_modified_a = obj.measure_a
            obj.measure_modified_b = obj.measure_b
            obj.measure_modified_c = obj.measure_c
            obj.measure_modified_d = obj.measure_d
        else:
            # Check whether offset should be updated
            curr = obj.datetime
            prev = device.latest_datetime

            if (curr - prev).seconds > 10 * 60:
                prev = Measurement.objects.filter(device_id=obj.device_id).latest('datetime')
                device.params['offset'] = [prev.measure_modified_a,
                                           prev.measure_modified_b,
                                           prev.measure_modified_c,
                                           prev.measure_modified_d]

            # Update device's latest_datetime
            device.latest_datetime = obj.datetime
            device.save()

            offset = device.params.get('offset', [0, 0, 0, 0])
            obj.measure_modified_a = obj.measure_a + offset[0]
            obj.measure_modified_b = obj.measure_b + offset[1]
            obj.measure_modified_c = obj.measure_c + offset[2]
            obj.measure_modified_d = obj.measure_d + offset[3]

        obj.save()
        return obj


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'device_id', 'device_type', 'params')
