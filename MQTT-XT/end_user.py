# -*- coding: utf-8 -*-

import os
import shutil
import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import psutil
from numpy import long

# model girdilerini almak için 2D bir dizi oluşturulsu- dolu değerleri bu diziliere alınıp modele verielcek


sub_message_type = dict(get_reachability="0", get_info_drone="1", get_commanmd_result="2")

global sub_message

# pragma CONFIG
client_ID = "end_user"

test_packet_length = 5

broker_cloud_address = "127.0.0.1" # bu clientta etki etmıyor
broker_cloud_port = 1883

#topics
client_sub_topic_reachable = "fog1/reachable"
client_sub_topic_drone1_state_topic = "fog1/drone1/state"
client_sub_topic_drone2_state_topic = "fog1/drone2/state"
client_sub_topic_qdos_topic = "fog1/QDoS"

fog1_list=[]
drone1_reachability_changed=False
drone2_reachability_changed=False

cloud_connect=True

client_pub_topic_connection = "init/fog1"


publish_delay_time = 1
publish_size = 50
client_number = "FOG1"
location_number = "L1"
packet_name=location_number+ "-"+ client_number

dir_name = "data_log1"
log_dir = os.getcwd()
log_dir = log_dir + "/" + dir_name


if os.path.isdir(log_dir):
    print("File exist")
    shutil.rmtree(log_dir, ignore_errors=True)
    log_dir = log_dir + "/"
    os.mkdir(log_dir)
else:
    log_dir = log_dir + "/"
    os.mkdir(log_dir)



def process_reachability(sub_message):
    print("Sub message:", sub_message)
    global drone1_reachability_changed
    global drone2_reachability_changed

    if(sub_message=="drone1/reachable" and drone1_reachability_changed==False):
        fog1_list.append("drone1")
        drone1_reachability_changed =True
    elif(sub_message=="drone2/reachable" and drone2_reachability_changed==False):
        fog1_list.append("drone2")
        drone2_reachability_changed = True

    if(sub_message=="drone1/unreachable" and drone1_reachability_changed==True):
        fog1_list.remove("drone1")
        drone1_reachability_changed =False
    elif(sub_message=="drone2/unreachable" and drone2_reachability_changed==True):
        fog1_list.remove("drone2")
        drone2_reachability_changed = False

    fog1_list.sort()
    print(fog1_list)
    # These code snippet provides that it handles time by incoming messages and saves them to file.
    # After this operation, it prepares new message.
    #start_time_for_message_log = long(time.time() * 1000)
    #time_first, message_time = sub_message.split("[")
    #message_time, unused = message_time.split("]")
    #unused, time_last = sub_message.split("]")
    #incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
    #write_cpu_mem_values()
    #new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
    #publish_message_log_time(time_first, start_time_for_message_log, new_message.__sizeof__())
    #publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)

    #print("Publish NoNaN:", new_message)

    publish.single(client_pub_topic_connection, "", 1, False, broker_cloud_address, broker_cloud_port)

def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    process_reachability(sub_message)


def client_sub_pub():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client(client_ID)  # create new instance
    print("connecting to broker")

    client.connect(broker_cloud_address)  # connect to broker

    client.subscribe(client_sub_topic_reachable)
    client.subscribe(client_sub_topic_drone1_state_topic)
    client.subscribe(client_sub_topic_drone2_state_topic)
    client.subscribe(client_sub_topic_qdos_topic)
    while (1):
        client.loop_start()  # start the loop
        # attach function to callback
        client.on_message = callback_on_message
        client.loop_stop()  # stop the loop

def client_pub (connection_type):
    print("This client will be run for only publishing. \n ")
    #client = mqtt.Client(client_ID)  # create new instance
    global cloud_connect
    global broker_cloud_address
    global broker_cloud_port
    global client_pub_topic_connection
    print(cloud_connect)
    publish_message=""
    while (cloud_connect==True):
        if(connection_type=="connect"):
            print("connnectttt")
            publish_message = "connect"
            publish.single(client_pub_topic_connection, publish_message, 2, False, broker_cloud_address,
                           broker_cloud_port)
            client_sub_pub()
        elif(connection_type=="disconnect"):
            publish_message = "disconnect"


        print("Publish:", publish_message)





connection_type="connect"
client_pub(connection_type)

