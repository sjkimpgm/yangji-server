from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets

from .models import Message, MessageSerializer, Measurement, MeasurementSerializer


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


import datetime
import random
def generate_data(request):
    for d in range(1, 32):
        for h in range(0, 24):
            date = datetime.datetime(2019, 5, d, h, 0, 0)
            m = Measurement(datetime=date, measure_a=random.random(), measure_b=random.random(), measure_c=random.random(), measure_d=random.random())
            m.save()

def clear_data(request):
    Measurement.objects.all().delete()