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
    list_display = ('id', 'device_id', 'datetime', '__str__')
    search_fields = ['device_id']

    list_filter = ('device_id', ('datetime', DateTimeRangeFilter))


admin.site.register(Measurement, MeasurementAdmin)
