from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.contrib.postgres import fields

from .models import Measurement, Device

# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_id', 'device_type')
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Device, DeviceAdmin)

admin.site.register(Measurement)
