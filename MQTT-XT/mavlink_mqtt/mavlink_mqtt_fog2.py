import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
client_ID = "fog2"
fog_name= "fog2"

broker_fog_address = "127.0.0.1" # bu clientta etki etmıyor
broker_fog_port = 1883

broker_cloud_address = "127.0.0.1" # bu clientta etki etmıyor
broker_cloud_port = 1883

def publish_to_cloud(publish_topic,publish_message):
    publish.single(publish_topic, publish_message, 2, False, broker_cloud_address, broker_cloud_port)

def process_sub_message_cloud(message,topic):


    print(topic+":"+message)
    publish_to_cloud(fog_name+"/"+topic,message)



def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_cloud(sub_message,topic)


client = mqtt.Client(client_ID)  # create new instance
print("connecting to Cloud\n")

client.connect(broker_fog_address,broker_fog_port)  # connect to broker

client.subscribe("uav4/#")
client.subscribe("uav5/#")
client.subscribe("uav6/#")

while (1):
    client.loop_start()  # start the loop
    # attach function to callback
    client.on_message = callback_on_message_cloud
    client.loop_stop()  # stop the loop