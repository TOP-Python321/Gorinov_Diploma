from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
import json
import time


from .models import Device
from .tasks import mqtt_test
from django.http import (
    HttpResponse, 
    HttpResponsePermanentRedirect, 
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound
)
from .mqtt import mqtt_publish
from .models import Device, DeviceType, Scenario
from .import forms

# Create your views here.
def to_get_data(request):
    """Запуск задачи приема сообщений с устройств."""
    mqtt_test.delay()    
    return HttpResponse("<h2>Запуск цикла опроса датчиков</h2>")
   
# def devices(request):
   
    # devices = Device.objects.all()    
    # # linkquality = {json.loads(device.json_data) for device in devices}
    # # print(linkquality)
    # devices_param = {}
    # for device in devices:
        # device_dict = json.loads(device.json_data)
        # devices_param |= {device.address: device_dict}
    # context = {
       # 'devices': devices,
       # 'devices_param': devices_param
    # }
    
    # return render(request, 'smart_house/devices.html', context)
    
class DeviceListView(ListView):
    model = Device
    # путь к шаблону
    template_name = 'smart_house/devices.html'
    # переопределение имени 'object_list'
    context_object_name = 'devices'
    
    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)       
        for obj in self.object_list:            
            obj.json_data = json.loads(obj.json_data)
        return context
        
class DeviceDetailView(DetailView):
    model = Device
    template_name = 'smart_house/device.html'
    context_object_name = 'device'
    
    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)       
        self.object.json_data = json.loads(self.object.json_data)
        context['device_type'] = DeviceType.objects.get(id=self.object.devices_type_id)        
        return context
        
def socket_220(request):
    """
        Принимает через метод POST состояние устройства. Передает команду устройству 
        через вызов фукции mqtt_publish.
    """
    if request.method == 'POST':
        device = Device.objects.get(id=request.POST.get('id'))
        msg = 'ON' if request.POST.get('state') == 'OFF' else 'OFF'         
        mqtt_publish(device.address, msg)
    return redirect('device', device.id)
    
def wate_pump_form(request):

    if request.method == "POST":
        # создание экземпляра формы
        form = forms.WaterPumpForm(request.POST)        
        if form.is_valid():
            scenario = Scenario(
                name=form.cleaned_data["name"], 
                water_leak_sensor=form.cleaned_data["water_leak_sensor"],
                socket_220=form.cleaned_data["socket_220"],
                scenario_type=form.cleaned_data["scenario_type"],
            )           
            scenario.save()           
    elif request.method == 'GET':
        form = forms.WaterPumpForm()    
    context = {
        "form": form,        
    }
    print(context)
    return render(request, 'smart_house/wate_pump_form.html', context)