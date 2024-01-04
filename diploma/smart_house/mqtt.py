# про paho.mqtt
# http://www.steves-internet-guide.com/mqtt-python-beginners-course/

from core.settings import MQTT_PORT, MQTT_HOSTS
from paho.mqtt import publish, client
import json

def mqtt_publish(address: str, msg: str) -> None:
    """Принимет адрес устройства и команду. Отправляет сообщение устройству."""
    obj = client.Client()
    obj.connect(MQTT_HOSTS, MQTT_PORT)   
    obj.publish(f'zigbee2mqtt/{address}/set', json.dumps({ 'state': msg }))

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

