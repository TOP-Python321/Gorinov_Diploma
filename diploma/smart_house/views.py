import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, FormView
from .tasks import in_mqtt
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
from .forms import WaterPumpForm, DeviceForm
from .import forms

# Create your views here.


def to_get_data(request):
    """Запуск задачи приема сообщений с устройств."""

    in_mqtt.delay()
    # HTTP_REFERER: страница с которой был получен запрос
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)

    
    
def connect_decvice(request):
    """Отправляет на zigbee2mqtt сообщение c разрешеним на подключения новых устройств"""

    mqtt_publish('zigbee2mqtt/bridge/request/permit_join', {"value": "true", "time": 20})
    # HTTP_REFERER: страница с которой был получен запрос
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)
    

def index(request):
    return render(request, 'smart_house/index.html')
    
class DeviceListView(ListView):
    """Описывает представление эземпляров устройств"""

    model = Device
    # путь к шаблону
    template_name = 'smart_house/devices.html'
    # переопределение имени 'object_list'
    context_object_name = 'devices'
    
    def get_context_data(self, **kwargs) -> dict:
        """переопределяет json_data у экземпляров"""
        context = super().get_context_data(**kwargs)       
        for obj in self.object_list:            
            obj.json_data = json.loads(obj.json_data)
        return context

        
class DeviceDetailView(DetailView):
    """Описывает представление устройства"""

    model = Device
    template_name = 'smart_house/device.html'
    context_object_name = 'device'
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)       
        self.object.json_data = json.loads(self.object.json_data)
        context['device_type'] = DeviceType.objects.get(id=self.object.devices_type_id)       
        return context
        
        
class DeviceUpdateView(UpdateView):
    """Описывает класс редактирования устройства"""

    model = Device
    form_class = DeviceForm
    template_name = 'smart_house/device_edit.html'

    
class DeviceDeleteView(DeleteView):
    """Описывает класс для удаления устройства"""

    model = Device
    form_class = DeviceForm
    template_name = 'smart_house/device_del.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # удаления устройства из zigbee2mqtt        
        mqtt_publish('zigbee2mqtt/bridge/request/device/remove', {'id': self.get_object().address})
        self.get_object().delete()      
        return redirect('devices')   

        
class ScenarioListView(ListView):
    """Описывает представление стратегий"""

    model = Scenario
    template_name = 'smart_house/scenarios.html'
    context_object_name = 'scenarios'

class ScenarioDetailView(DetailView):
    """Описывает представление стратегии"""

    model = Scenario
    template_name = 'smart_house/scenario.html'
    context_object_name = 'scenario'


class WaterPumpScenarioFormView(FormView):   
    """Описывает класс создания сценария <<насосная станция>>"""

    form_class = WaterPumpForm
    template_name = 'smart_house/water_pump_scenarios_new.html'

    def form_valid(self, form) -> HttpResponse:
        scenario = Scenario(
            name=form.cleaned_data["name"],
            scenario_type=form.cleaned_data["scenario_type"],
        )
        scenario.save()
        for device in form.cleaned_data["water_leak_sensor"]:
            scenario.devices.add(device)
        scenario.devices.add(form.cleaned_data["socket_220"])
        return redirect("scenario", scenario.pk)
       
    
class WaterPumpScenarioUpdateView(UpdateView):
    """Описывает класс редактирования сценария"""

    model = Scenario
    form_class = WaterPumpForm
    template_name = 'smart_house/water_pump_scenarios_new.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Возвращает заполненную форму с данными конкретного сценария"""
        form = forms.WaterPumpForm(
            initial={
                "name": self.get_object().name,
                "water_leak_sensor": self.get_object().devices.filter(devices_type__name="Датчик протечки воды"),
                "socket_220": self.get_object().devices.get(devices_type__name="socket_220"),
                "scenario_type": self.get_object().scenario_type
            })    
        context = {
            "form": form,        
        }   
        return render(request, self.template_name, context)

    def form_valid(self, form) -> HttpResponseRedirect:
        self.object.name = form.cleaned_data["name"]
        self.object.scenario_type = form.cleaned_data["scenario_type"]
        self.object.devices.clear()
        for device in form.cleaned_data["water_leak_sensor"]:
            self.object.devices.add(device)
        self.object.devices.add(form.cleaned_data["socket_220"])
        self.object.save()
        return redirect("scenario", self.object.pk)


class WaterPumpScenarioDeleteView(DeleteView):
    """Описывает класс удаления сценария"""

    model = Scenario
    form_class = WaterPumpForm    
   
    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
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
        mqtt_publish(f'zigbee2mqtt/{device.address}/set', msg)
    return redirect('device', device.id)
