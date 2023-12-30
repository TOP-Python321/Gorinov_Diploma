from django.shortcuts import render
import time
from .tasks import mqtt_test
from django.http import (
    HttpResponse, 
    HttpResponsePermanentRedirect, 
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound
)

from .models import Device
import json

# Create your views here.
def to_get_data(request):
    mqtt_test.delay()    
    return HttpResponse("<h2>Запуск цикла опроса датчиков</h2>")
    
def test(request):    
    data_to = {'data': str(data)}
    print(data)
    return render(request, 'smart_house/test.html', context=data_to)
    
def devices(request):
   
    devices = Device.objects.all()    
    # linkquality = {json.loads(device.json_data) for device in devices}
    # print(linkquality)
    devices_param = {}
    for device in devices:
        device_dict = json.loads(device.json_data)
        devices_param |= {device.address: device_dict}
    context = {
       'devices': devices,
       'devices_param': devices_param
    }
    
    return render(request, 'smart_house/devices.html', context)