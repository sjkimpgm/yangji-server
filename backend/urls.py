"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api import views
from .api.views import index_view
from .api.viewsets import *

router = routers.DefaultRouter()
router.register('measurement', MeasurementViewSet, basename="measurement")
router.register('device', DeviceViewSet)

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('api/generate_data/', views.generate_data),
    path('api/calc_device/', views.calc_device),

    path('api/measurement_dates/', views.measurement_dates),
    path('api/measurement_recent/', views.measurement_recent),
    path('api/measurement_aggr/', views.measurement_aggr),
    path('api/measurement_fill_diff/', views.measurement_fill_diff),
]


