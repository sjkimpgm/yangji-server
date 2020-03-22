from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.contrib.postgres import fields
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import Measurement, Device

# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_id', 'device_type')
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Device, DeviceAdmin)


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'get_device_name', 'datetime', '__str__')
    search_fields = ['device_id']

    list_filter = ('device_id', ('datetime', DateTimeRangeFilter))

    def get_device_name(self, obj):
        return Device.objects.get(device_id=obj.device_id).name


admin.site.register(Measurement, MeasurementAdmin)
