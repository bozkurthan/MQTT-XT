import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
client_ID = "end_user"

broker_cloud_address = "test.mosquitto.org" # bu clientta etki etmıyor
broker_cloud_port = 1883


def publish_to_fog(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, broker_cloud_address, broker_cloud_port)

i=0
while i<2000:
    now = datetime.datetime.utcnow()
    #now_local = datetime.datetime.now()
    #print(now_local)
    #publish_to_fog("hallowen", str(now_local))
    #epoch = datetime.datetime.utcfromtimestamp(0)

    milliseconds = now.timestamp() * 1000.0
    print(milliseconds)

    publish_to_fog("hallowen",milliseconds)
    i+=1
    time.sleep(1)