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
from .data import mqtt_publish
from .models import Device, DeviceType, Scenario
from .forms import WaterPumpForm
from .import forms

# Create your views here.
def to_get_data(request):
    """Запуск задачи приема сообщений с устройств."""
    mqtt_test.delay()    
    return HttpResponse("<h2>Запуск цикла опроса датчиков</h2>")

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