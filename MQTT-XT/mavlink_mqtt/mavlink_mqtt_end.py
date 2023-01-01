import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
client_ID = "end_user"

broker_cloud_address = "127.0.0.1"#"test.mosquitto.org" # bu clientta etki etmıyor
broker_cloud_port = 1883


def process_sub_message_cloud(message,topic):


    print(topic+":"+message)



def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_cloud(sub_message,topic)


client = mqtt.Client(client_ID)  # create new instance
print("connecting to Cloud\n")

client.connect(broker_cloud_address,broker_cloud_port)  # connect to broker

client.subscribe("fog1/#")
client.subscribe("fog2/#")

while (1):
    client.loop_start()  # start the loop
    # attach function to callback
    client.on_message = callback_on_message_cloud
    client.loop_stop()  # stop the loop