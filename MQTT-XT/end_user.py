# -*- coding: utf-8 -*-
#region imports
import os
import shutil
import threading
import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import datetime
import psutil
#endregion


# region MQTT connection Variables
client_ID = "end_user"

broker_cloud_address = "127.0.0.1" # bu clientta etki etmıyor
broker_cloud_port = 1883

#endregion


#region Topics

#region Topics to Publish

#topics pub to cloud

#Connectivity
cli_pub_topic_connection = "init/"

#Command
cli_to_cloud_pub_top_d1_cmd="fog1/drone1/commands"
cli_to_cloud_pub_top_d2_cmd="fog1/drone2/commands"
cli_to_cloud_pub_top_fog_cmd="fog1/commands"

#endregion

#region Topics to Subscribe

#Connectivity
cli_to_cloud_sub_top_reach = "fog1/reachable"

#Drone states
cli_to_cloud_sub_top_d1_state = "fog1/drone1/state/#"
cli_to_cloud_sub_top_d2_state = "fog1/drone2/state/#"
cli_to_cloud_sub_top_qdos = "fog1/QDoS"

#Command Results
cli_to_cloud_sub_top_d1_cmd_result = "fog1/drone1/commands_result/#"
cli_to_cloud_sub_top_d2_cmd_result = "fog1/drone2/commands_result/#"

#endregion

#endregion



fog1_list=[]
drone1_reachability_changed=False
drone2_reachability_changed=False

cloud_connect=True


publish_delay_time = 1
publish_size = 50
client_number = "FOG1"
location_number = "L1"
packet_name=location_number+ "-"+ client_number


#region data log
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
#endregion

# region Function definitions

def process_sub_message_cloud(message,topic):
    print("Cloud Topic:"+topic,",Message:"+message)

    if(topic=="fog1/#"):
    #sub to Connectivity
        if(topic=="fog1/drone1/reachable"):
            print("Reacheability of drone1:", message)
        elif(topic=="fog1/drone2/reachable"):
            print("Reacheability of drone2:", message)
        #sub to drone states
        elif (topic == "drone1/state/#"):
            print(topic +":" +message)
            now_local = datetime.datetime.now()
            print(now_local)
        elif (topic == "drone2/state/#"):
            print(topic + ":" + message)
            now_local = datetime.datetime.now()
            print(now_local)


# message function that handle cloud messages
def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_cloud(sub_message,topic)


def cloud_pub_connect_message(fog_number,connection_type):


    if(connection_type=="connect"):
        print("This client connects %s, on cloud. \n " %fog_number)
        publish_message = "connect"
        publish.single(cli_pub_topic_connection+fog_number, publish_message, 2, False, broker_cloud_address,
                       broker_cloud_port)
    elif(connection_type=="disconnect"):
        publish_message = "disconnect"


    print("Publish:", publish_message)


def publish_to_cloud_all():
    print("pub")

def func_sub_pub(thread_type):

    if (thread_type == "Subscribe_Cloud"):

        print("This client will subscribe to Cloud broker. \n ")
        client = mqtt.Client(client_ID)  # create new instance
        print("connecting to Cloud\n")

        client.connect(broker_cloud_address,broker_cloud_port)  # connect to broker

        client.subscribe(cli_to_cloud_sub_top_qdos)
        client.subscribe(cli_to_cloud_sub_top_reach)
        client.subscribe(cli_to_cloud_sub_top_d1_state)
        client.subscribe(cli_to_cloud_sub_top_d2_state)
        client.subscribe(cli_to_cloud_sub_top_d1_cmd_result)
        client.subscribe(cli_to_cloud_sub_top_d2_cmd_result)
        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message_cloud
            client.loop_stop()  # stop the loop

    elif(thread_type=="Publish_Cloud"):
        print("This thread will publish messages to Cloud. \n ")
        while (1):
            publish_to_cloud_all()


def publish_to_cloud(publish_topic,publish_message):
    publish.single(publish_topic, publish_message, 2, False, broker_cloud_address, broker_cloud_port)

class sub_pub_thread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      func_sub_pub(self.name)
      print ("Exiting " + self.name)

#endregion


# region Main class

def main():

    cloud_pub_connect_message("fog1","connect")

    now = datetime.datetime.utcnow()
    now_local = datetime.datetime.now()
    print(now_local)
    i=0
    while i<100:

        time.sleep(1)
        i += 1
        publish_to_cloud(cli_to_cloud_pub_top_d1_cmd,"offboard,70")
        print("offboard,70 " + str(i) + " seq")

    now = datetime.datetime.utcnow()
    now_local = datetime.datetime.now()
    print(now_local)
    sub_cloud_thread = sub_pub_thread(1, "Subscribe_Cloud")
    #pub_cloud_thread = sub_pub_thread(2, "Publish_Cloud")

    sub_cloud_thread.start()
    #pub_cloud_thread.start()

    sub_cloud_thread.join()
    #pub_cloud_thread.join()


#endregion

# region Code start
if __name__ == '__main__':
    main()
# endregion

