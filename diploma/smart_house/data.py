# про paho.mqtt
# http://www.steves-internet-guide.com/mqtt-python-beginners-course/
from abc import ABC, abstractmethod
from core.settings import MQTT_PORT, MQTT_HOSTS
from paho.mqtt import publish, client
import json

from .import models


def mqtt_publish(topic: str, msg: dict) -> None:
    """Принимает topic и команду. Отправляет сообщение устройству."""
    obj = client.Client()
    obj.connect(MQTT_HOSTS, MQTT_PORT)   
    obj.publish(topic, json.dumps(msg))


class Strategy(ABC):
    """Абстрактный класс стратегий действий на основании сценария."""   
    water_type = models.DeviceType.objects.get(name="Датчик протечки воды")
    socket_type = models.DeviceType.objects.get(name="socket_220")
    
    @abstractmethod
    def action(self, scenario: models.Scenario) -> None:
        ...

        
class PumpingStationStrategy(Strategy):
    """Описывает стратегию для сценария <<Насосная станция>>"""    
   
    def action(self, scenario: models.Scenario) -> None:
        print(f'DEBUG передана стратегия {scenario = }')       
        water_leak = scenario.devices.filter(devices_type=self.water_type)
        socket_220 = scenario.devices.get(devices_type=self.socket_type)        
        if (
            any(json.loads(dev.json_data)["water_leak"] for dev in water_leak)
            and json.loads(socket_220.json_data)["state"] == "ON"
        ):
            print("DEBUG - выключить розетку")            
            mqtt_publish(f'zigbee2mqtt/{socket_220.address}/set', {'state': "OFF"})
