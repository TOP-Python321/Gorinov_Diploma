# пор pano.mqtt
# http://www.steves-internet-guide.com/mqtt-python-beginners-course/

from paho.mqtt import publish, client as mqtt
import json
import time

broker_address="192.168.1.6"

data = {}
client = mqtt.Client()
client.connect(broker_address, 1883)
msg = json.dumps({ 'state': 'OFF' })
client.publish('zigbee2mqtt/0xa4c13808f7338468/set', msg)

def on_message(client, userdata, message):
    # print("message received " ,type(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    data[''.join(message.topic.split('/')[-1])] = json.loads(message.payload.decode("utf-8"))
    print(data)

client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
# client.loop_start() #start the loop
client.subscribe("zigbee2mqtt/+")
client.publish('zigbee2mqtt/0xa4c13808f7338468/set', json.dumps({ 'state': 'ON' }))
time.sleep(4) # wait
client.loop_stop() #stop the loop
# client.loop_forever()

