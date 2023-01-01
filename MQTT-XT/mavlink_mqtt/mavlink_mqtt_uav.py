import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
client_ID = "uav_client1"
uav_topic="uav1"

broker_fog_address = "127.0.0.1" # bu clientta etki etmıyor
broker_fog_port = 1883

def publish_to_fog(publish_topic,publish_message):
    publish.single(publish_topic, publish_message, 2, False, broker_fog_address, broker_fog_port)

i=0
while i<100:
    print(uav_topic+", Current "+str(i)+". data is sent")
    publish_to_fog(uav_topic+"/light_sensor/","784")
    time.sleep(0.5)
    publish_to_fog(uav_topic+"/temp_sensor/","25.7")
    time.sleep(0.5)
    publish_to_fog(uav_topic+"/humidity/","80.9")
    time.sleep(0.5)
    i+=1

publish_to_fog("last","end "+uav_topic)