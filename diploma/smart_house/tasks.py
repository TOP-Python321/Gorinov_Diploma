from django.core.exceptions import ObjectDoesNotExist
from paho.mqtt import publish, client as mqtt

from core.settings import MQTT_PORT, MQTT_HOSTS
from core.celery import app
from .models import Device, DeviceType, Scenario
from .import data

@app.task
def in_mqtt():
    """Получает параметры датчиков и записывает их в базу данных."""

    def on_message(client, userdata, message):
        print(f'DEBUG {message.payload.decode("utf-8")}')
        try:
            device = Device.objects.get(address=''.join(message.topic.split('/')[-1]))
        except ObjectDoesNotExist:
            print(f'DEBUG <новое устройство>')
            device = Device(name='новое устройство', address=''.join(message.topic.split('/')[-1]))
            devices_type = DeviceType.objects.get(name="Новое устройство")
            device.devices_type_id = devices_type.id
            device.json_data = message.payload.decode("utf-8")
            # сохранение только устройства с json данными
            if message.payload:
                device.save()
        else:
            device.json_data = message.payload.decode("utf-8")
            device.save()
            print(f'DEBUG {device.devices_type = }')
            # выбор стратегии
            try:
                scena = Scenario.objects.get(devices=device)
                print(f'DEBUG имя типа стратегии -> {scena.scenario_type.name = }')
                if scena.scenario_type.name == "Насосная станция":
                    elem = data.PumpingStationStrategy()
                    print(f'{elem.water_type = }')
                    elem.action(scena)
            except Exception:
                pass            

    client = mqtt.Client()    
    client.on_message = on_message
    client.connect(MQTT_HOSTS)     
    client.subscribe("zigbee2mqtt/+")    
    client.loop_forever()
