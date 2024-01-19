# про paho.mqtt
# http://www.steves-internet-guide.com/mqtt-python-beginners-course/
from abc import ABC, abstractmethod
from core.settings import MQTT_PORT, MQTT_HOSTS
from paho.mqtt import publish, client
import json

from django.core.exceptions import ObjectDoesNotExist

from .import models

def mqtt_publish(address: str, msg: dict) -> None:
    """Принимает адрес устройства и команду. Отправляет сообщение устройству."""
    obj = client.Client()
    obj.connect(MQTT_HOSTS, MQTT_PORT)   
    obj.publish(f'zigbee2mqtt/{address}/set', json.dumps(msg))
    
def mqtt_all_publish(topic: str, msg: dict) -> None:
    obj = client.Client()
    obj.connect(MQTT_HOSTS, MQTT_PORT)   
    obj.publish(topic, json.dumps(msg))

class Strategy():
    """Абстрактный класс стратегий действий на основании сценария."""   
    water_type = models.DeviceType.objects.get(name="Датчик протечки воды")
    socket_type = models.DeviceType.objects.get(name="socket_220")
    
    @abstractmethod
    def action(scenario):
        ...
        
class PumpingStationStrategy(Strategy):
    """Описывает стратегию для сценария <<Насосная станция>>"""    
   
    def action(self, scenario: models.Scenario):
        print(f'DEBUG передана стратегия {scenario = }')       
        water_leak = scenario.devices_id.filter(devices_type=self.water_type)
        socket_220 = scenario.devices_id.get(devices_type=self.socket_type)
        
        if (
            any(json.loads(dev.json_data)["water_leak"] for dev in water_leak)
            and json.loads(socket_220.json_data)["state"] == "ON"
        ):
            print("DEBUG - выключить розетку")            
            mqtt_publish(socket_220.address, {'state': "OFF"})            
       
            
class СhoiceStrategy:
    """Описывает выбор стратегии на основании полученного объекта <<device>>."""
    def to_strategy(device: models.Device):        
        if device.devices_type.name == "Датчик протечки воды":
            try:
                PumpingStationStrategy.action(device.scenarios_as_water_leak_sensor)
            except ObjectDoesNotExist:
                print("DEBUG - yстройство не входит в стратегию")
        if device.devices_type.name == "socket_220":
            try:
                PumpingStationStrategy.action(device.scenarios_as_socket_220)
            except ObjectDoesNotExist:
                print("DEBUG - yстройство не входит в стратегию")
    
# def on_message(client, userdata, message):
    # data_1 = {}
    # # print("message received " ,type(message.payload.decode("utf-8")))
    # # print("message topic=",message.topic)
    # data_1[''.join(message.topic.split('/')[-1])] = json.loads(message.payload.decode("utf-8"))    
    # print(data_1)

# client.on_message=on_message #attach function to callback
# client.connect(broker_address) #connect to broker
# # client.loop_start() #start the loop
# client.subscribe("zigbee2mqtt/+")
# client.publish('zigbee2mqtt/0xa4c13808f7338468/set', json.dumps({ 'state': 'ON' }))
# time.sleep(6) # wait
# # client.loop_stop() #stop the loop
# client.loop_forever()

