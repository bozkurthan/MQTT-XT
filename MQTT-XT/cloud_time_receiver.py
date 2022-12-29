import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
client_ID = "end_user"

broker_cloud_address = "test.mosquitto.org" # bu clientta etki etmıyor
broker_cloud_port = 1883


def process_sub_message_cloud(message,topic):
    #print("Cloud Topic:"+topic,",Message:"+message)
    #now_local = datetime.datetime.now()
    #print(now_local)

    now = datetime.datetime.utcnow()
    milliseconds = now.timestamp() * 1000.0

    #print(milliseconds)

    print(int(float(milliseconds))-int(float(message)))


def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_cloud(sub_message,topic)


client = mqtt.Client(client_ID)  # create new instance
print("connecting to Cloud\n")

client.connect(broker_cloud_address,broker_cloud_port)  # connect to broker

client.subscribe("hallowen")
while (1):
    client.loop_start()  # start the loop
    # attach function to callback
    client.on_message = callback_on_message_cloud
    client.loop_stop()  # stop the loop