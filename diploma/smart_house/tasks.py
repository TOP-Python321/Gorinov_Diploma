from paho.mqtt import publish, client as mqtt
import json
import time

from core.settings import MQTT_PORT, MQTT_HOSTS
from core.celery import app 
from .models import Device

@app.task
def mqtt_test():
    """Получает параметры датчиков и записывает их в базу данных."""

    def on_message(client, userdata, message):        
        devices = Device.objects.get(address=''.join(message.topic.split('/')[-1]))
        devices.json_data = message.payload.decode("utf-8")
        devices.save()        
        print(devices.name)

    client = mqtt.Client()    
    client.on_message=on_message #attach function to callback
    client.connect(MQTT_HOSTS) #connect to broker
    # client.loop_start() #start the loop
    client.subscribe("zigbee2mqtt/+")   
    time.sleep(4) # wait
    # client.loop_stop() #stop the loop
    client.loop_forever()