# -*- coding: utf-8 -*-

import os
import shutil
import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import psutil
from numpy import long

# model girdilerini almak için 2D bir dizi oluşturulsu- dolu değerleri bu diziliere alınıp modele verielcek


global sub_message

# pragma CONFIG
client_ID = "end_user"

test_packet_length = 5

broker_cloud_address = "127.0.0.1" # bu clientta etki etmıyor
broker_cloud_port = 1883

#topics
client_sub_topic = "test-fog1"
client_pub_topic = "test-cloud"


publish_delay_time = 0
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



def data_process_to_pub(sub_message):
    print("Sub message:", sub_message)

    # These code snippet provides that it handles time by incoming messages and saves them to file.
    # After this operation, it prepares new message.

    print("No NaN value, so directly publish.")
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

    new_message="test"
    publish.single(client_pub_topic, new_message, 1, False, broker_cloud_address, broker_cloud_port)

def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    data_process_to_pub(sub_message)

def client_sub_pub():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client(client_ID)  # create new instance
    print("connecting to broker")

    client.connect(broker_cloud_address)  # connect to broker
    client.subscribe(client_sub_topic)
    while (1):
        client.loop_start()  # start the loop
        # attach function to callback
        client.on_message = callback_on_message
        client.loop_stop()  # stop the loop

def client_pub ():
    print("This client will be run for only publishing. \n ")
    client = mqtt.Client(client_ID)  # create new instance


    print("Without model message process")
    i=0
    while (i<publish_size):
        start_time_for_message_log = long(time.time() * 1000)
        data_message1= "tete"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
        data_message2= "tete" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
        data_message3= "tete"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA

        publish_message = "( (" + location_number + "-" + client_number + "-" + str(i) + ".Paket), (" + str(long(
            time.time() * 1000)) + "), ( ( Data: (Light: " + data_message1 + ", Humidity: " + data_message2 + ", Temperature:" + data_message3 + ") ) )"
        publish.single(client_pub_topic, publish_message, 1, False, broker_cloud_address, broker_cloud_port)

        time.sleep(publish_delay_time)
        print("Publish:", publish_message)
        i = i + 1


client_sub_pub()

#    client_pub()