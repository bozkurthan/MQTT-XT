# -*- coding: utf-8 -*-

import threading

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish

# model girdilerini almak için 2D bir dizi oluşturulsu- dolu değerleri bu diziliere alınıp modele verielcek


sub_message_type = dict(get_reachability="0", get_info_drone="1", get_commanmd_result="2")

global sub_message

# pragma CONFIG
client_ID = "activator_client"

#adress definition
broker_cloud_address = "test.mosquitto.org"
broker_cloud_port = 1883
broker_fog1_address = "192.168.1.41"
broker_fog1_port = 1884



#topics sub to fog broker
client_sub_topic_drone1 = "drone1/state/#"
client_sub_topic_drone2 = "drone2/state/#"

#topics sub to cloud
client_sub_topic_connection = "init/fog1"

#topics pub to cloud
client_pub_topic_drone1_state="fog1/drone1/state"


cloud_connect=True



exitFlag = 0
def process_reachability(sub_message):
    print("Sub message:", sub_message)


    if(sub_message=="connect"):
        print("Connect_message_received:", sub_message)
    elif(sub_message != ""):
        if (sub_message[0] == "L"):
            print("Published LOcation: "+ sub_message)
            publish.single(client_pub_topic_drone1_state+"/location", sub_message, 1, False, broker_cloud_address, broker_cloud_port)
        if (sub_message[0] == "B"):
            print("Published LOcation: " + sub_message)
            publish.single(client_pub_topic_drone1_state+"/battery", sub_message, 1, False, broker_cloud_address, broker_cloud_port)

        # These code snippet provides that it handles time by incoming messages and saves them to file.
    # After this operation, it prepares new message.


    #publish.single(client_pub_topic_connection, "", 1, False, broker_cloud_address, broker_cloud_port)

def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    process_reachability(sub_message)


def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    process_reachability(sub_message)

def client_pub ():
    print("This client will be run for only publishing. \n ")
    #client = mqtt.Client(client_ID)  # create new instance
    global cloud_connect
    global broker_cloud_address
    global broker_cloud_port
    global client_pub_topic_connection
    print(cloud_connect)
    publish_message=""
    while (cloud_connect==True):
        publish.single(client_pub_topic_connection, publish_message, 2, False, broker_cloud_address,broker_cloud_port)


        print("Publish:", publish_message)

def client_sub_pub(sub_type):
    if (sub_type == "Subscribe_Broker"):
        print("This client will subscribe to own broker. \n ")

        client2 = mqtt.Client(client_ID)  # create new instance
        print("connecting to Broker")

        client2.connect(broker_fog1_address)  # connect to broker

        client2.subscribe(client_sub_topic_drone1)
        client2.subscribe(client_sub_topic_drone2)
        while (1):
            client2.loop_start()  # start the loop
            # attach function to callback
            client2.on_message = callback_on_message_cloud
            client2.loop_stop()  # stop the loop

    if(sub_type=="Subscribe_Cloud"):
        print("This client will wait for connection signal. \n ")

        client = mqtt.Client(client_ID)  # create new instance
        print("connecting to Cloud")

        client.connect(broker_cloud_address)  # connect to broker
        client.subscribe(client_sub_topic_connection)

        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message
            client.loop_stop()  # stop the loop



class subscribe_thread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      client_sub_pub(self.name)
      print ("Exiting " + self.name)



# Create new threads
sub_cloud_thread = subscribe_thread(1, "Subscribe_Cloud")


sub_broker_thread = subscribe_thread(2, "Subscribe_Broker")


sub_broker_thread.start()
sub_cloud_thread.start()

sub_broker_thread.join()
sub_cloud_thread.join()
# Start new Threads


print ("Exiting Main Thread")










