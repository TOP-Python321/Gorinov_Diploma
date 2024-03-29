from django import forms
from .models import Scenario, Device, ScenarioType


class WaterPumpForm(forms.ModelForm):
    """
        Описывает форму для сценария "Насосная станция"
    """

    water_leak_sensor = forms.ModelMultipleChoiceField(
        queryset=Device.objects.filter(devices_type__name="Датчик протечки воды"),        
        label="Датчик протечки",
        help_text="Выберите датчик протечки",
    )    
    socket_220 = forms.ModelChoiceField(
        queryset=Device.objects.filter(devices_type__name="socket_220"), 
        empty_label=None,
        label="Розетка",
        help_text="Выберите розетку",
        
    )
    scenario_type = forms.ModelChoiceField(
        queryset=ScenarioType.objects.filter(name="Насосная станция"),        
        label="Тип сценария",
        help_text="Выберите тип сценария",
        empty_label=None
    )

    class Meta:
        model = Scenario
        fields = ["name"]

        
class DeviceForm(forms.ModelForm):
    """Описывает форму устройства"""
    
    class Meta:
        model = Device
        fields = ["name", "groups_id", "devices_type"]
