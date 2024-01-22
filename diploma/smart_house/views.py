from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
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
from .data import mqtt_publish, mqtt_all_publish
from .models import Device, DeviceType, Scenario
from .forms import WaterPumpForm, DeviceForm
from .import forms

# Create your views here.
def to_get_data(request):
    """Запуск задачи приема сообщений с устройств."""
    mqtt_test.delay()    
    return redirect('devices')
    
    
def connect_decvice(request):
    """Отправляетна zigbee2mqtt сообщение c разрешеним на подключения новых устройств"""
    mqtt_all_publish('zigbee2mqtt/bridge/request/permit_join', {"value": "true", "time": 20})
    return redirect('devices')
    

def index(request):
    return redirect('devices')
    
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
        
        
class DeviceUpdateView(UpdateView):
    """Описывает класс редактирования устройства"""
    model = Device
    # какой класс форм использовать
    form_class = DeviceForm
    template_name = 'smart_house/device_edit.html'
    
    
class DeviceDeleteView(DeleteView):
    """Описывает класс для удаления устройства"""
    model = Device
    # какой класс форм использовать
    form_class = DeviceForm
    template_name = 'smart_house/device_del.html'

    def get(self, request, *args, **kwargs):
        # удаления устройства из zigbee2mqtt        
        mqtt_all_publish('zigbee2mqtt/bridge/request/device/remove', {'id': self.get_object().address})
        self.get_object().delete()      
        return redirect('devices')   

        
class ScenarioListView(ListView):
    model = Scenario
    # путь к шаблону
    template_name = 'smart_house/scenarios.html'
    # переопределение имени 'object_list'
    context_object_name = 'scenarios'

class ScenarioDetailView(DetailView):
    model = Scenario
    template_name = 'smart_house/scenario.html'
    context_object_name = 'scenario'

class WaterPumpScenarioFormView(FormView):   
    # какой класс форм использовать
    form_class = WaterPumpForm
    template_name = 'smart_house/water_pump_scenarios_new.html'
    # success_url = ''
    def form_valid(self, form):       
            scenario = Scenario(
                name=form.cleaned_data["name"],                
                scenario_type=form.cleaned_data["scenario_type"],
            )
            scenario.save()
            for device in form.cleaned_data["water_leak_sensor"]:
                scenario.devices_id.add(device)
            scenario.devices_id.add(form.cleaned_data["socket_220"])
            return redirect("scenarios")
       
    
class WaterPumpScenarioUpdateView(UpdateView):
    model = Scenario
    # какой класс форм использовать
    form_class = WaterPumpForm
    template_name = 'smart_house/water_pump_scenarios_new.html'   
    def get(self, request, *args, **kwargs):
        form = forms.WaterPumpForm(
            initial={
                "name": self.get_object().name,
                "water_leak_sensor": self.get_object().devices_id.filter(devices_type__name="Датчик протечки воды"),
                "socket_220": self.get_object().devices_id.get(devices_type__name="socket_220"),
                "scenario_type": self.get_object().scenario_type
            })    
        context = {
            "form": form,        
        }   
        return render(request, self.template_name, context)
    def form_valid(self, form):            
            self.object.name = form.cleaned_data["name"]
            self.object.scenario_type=form.cleaned_data["scenario_type"]
            self.object.devices_id.clear()            
            for device in form.cleaned_data["water_leak_sensor"]:
                self.object.devices_id.add(device)
            self.object.devices_id.add(form.cleaned_data["socket_220"])            
            self.object.save()
            return redirect("scenarios")
    
class WaterPumpScenarioDeleteView(DeleteView):
    model = Scenario
    # какой класс форм использовать
    form_class = WaterPumpForm    
   
    def get(self, request, *args, **kwargs):
        self.get_object().delete()       
        return redirect('scenarios')    
        
def socket_220(request):
    """
        Принимает через метод POST состояние устройства. Передает команду устройству 
        через вызов фукции mqtt_publish.
    """
    if request.method == 'POST':
        device = Device.objects.get(id=request.POST.get('id'))
        msg = {'state': "ON"} if request.POST.get('state') == 'OFF' else {'state': "OFF"}         
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
            return redirect("scenarios")
    elif request.method == 'GET':
        form = forms.WaterPumpForm()    
    context = {
        "form": form,        
    }   
    return render(request, 'smart_house/wate_pump_form.html', context)