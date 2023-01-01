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
broker_cloud_port = 1885

#endregion


#region Topics

#region Topics to Publish

#topics pub to cloud

#Connectivity
cli_pub_topic_connection = "init/"

#Command
cli_to_cloud_pub_top_fog1_d1_cmd="fog1/drone1/commands"
cli_to_cloud_pub_top_fog1_d2_cmd="fog1/drone2/commands"
cli_to_cloud_pub_top_fog1_d3_cmd="fog1/drone3/commands"
cli_to_cloud_pub_top_fog2_d4_cmd="fog2/drone4/commands"
cli_to_cloud_pub_top_fog2_d5_cmd="fog2/drone5/commands"
cli_to_cloud_pub_top_fog2_d6_cmd="fog2/drone6/commands"



cli_to_cloud_pub_top_fog1_cmd="fog1/commands_all"
cli_to_cloud_pub_top_fog2_cmd="fog2/commands_all"

#endregion

#region Topics to Subscribe

#Connectivity
cli_to_cloud_sub_top_reach_fog1 = "fog1/reachable"
cli_to_cloud_sub_top_reach_fog2 = "fog2/reachable"


#Drone states
cli_to_cloud_sub_top_fog1_d1_state = "fog1/drone1/state/#"
cli_to_cloud_sub_top_fog1_d2_state = "fog1/drone2/state/#"
cli_to_cloud_sub_top_fog1_d3_state = "fog1/drone3/state/#"
cli_to_cloud_sub_top_fog2_d4_state = "fog2/drone4/state/#"
cli_to_cloud_sub_top_fog2_d5_state = "fog2/drone5/state/#"
cli_to_cloud_sub_top_fog2_d6_state = "fog2/drone6/state/#"


cli_to_cloud_sub_top_qdos_fog1 = "fog1/QDoS"
cli_to_cloud_sub_top_qdos_fog2 = "fog2/QDoS"

#Command Results
cli_to_cloud_sub_top_fog1_d1_cmd_result = "fog1/drone1/commands_result/#"
cli_to_cloud_sub_top_fog1_d2_cmd_result = "fog1/drone2/commands_result/#"
cli_to_cloud_sub_top_fog1_d3_cmd_result = "fog1/drone3/commands_result/#"
cli_to_cloud_sub_top_fog2_d4_cmd_result = "fog2/drone4/commands_result/#"
cli_to_cloud_sub_top_fog2_d5_cmd_result = "fog2/drone5/commands_result/#"
cli_to_cloud_sub_top_fog2_d6_cmd_result = "fog2/drone6/commands_result/#"

#endregion

#endregion






#endregion

# region Function definitions

def process_sub_message_cloud(message,topic):
    #print("Cloud Topic:"+topic,",Message:"+message)

    if(topic.startswith("fog1/drone1/commands_result")):
        print(topic,":",message)
    if(topic.startswith("fog1/drone2/commands_result")):
        print(topic,":",message)
    if(topic.startswith("fog1/drone3/commands_result")):
        print(topic,":",message)
    if(topic.startswith("fog2/drone4/commands_result")):
        print(topic,":",message)
    if(topic.startswith("fog2/drone5/commands_result")):
        print(topic,":",message)
    if(topic.startswith("fog2/drone6/commands_result")):
        print(topic,":",message)




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




def func_sub_pub(thread_type):

    if (thread_type == "Subscribe_Cloud"):

        print("This client will subscribe to Cloud broker. \n ")
        client = mqtt.Client(client_ID)  # create new instance
        print("connecting to Cloud\n")

        client.connect(broker_cloud_address,broker_cloud_port)  # connect to broker

        client.subscribe(cli_to_cloud_sub_top_qdos_fog1)
        client.subscribe(cli_to_cloud_sub_top_qdos_fog2)
        client.subscribe(cli_to_cloud_sub_top_reach_fog1)
        client.subscribe(cli_to_cloud_sub_top_reach_fog2)
        #fog1 area status
        client.subscribe(cli_to_cloud_sub_top_fog1_d1_state)
        client.subscribe(cli_to_cloud_sub_top_fog1_d2_state)
        client.subscribe(cli_to_cloud_sub_top_fog1_d3_state)
        #fog2 area status
        client.subscribe(cli_to_cloud_sub_top_fog2_d4_state)
        client.subscribe(cli_to_cloud_sub_top_fog2_d5_state)
        client.subscribe(cli_to_cloud_sub_top_fog2_d6_state)

        #fog1 area commands result
        client.subscribe(cli_to_cloud_sub_top_fog1_d1_cmd_result)
        client.subscribe(cli_to_cloud_sub_top_fog1_d2_cmd_result)
        client.subscribe(cli_to_cloud_sub_top_fog1_d3_cmd_result)
        #fog2 area commands result
        client.subscribe(cli_to_cloud_sub_top_fog2_d4_cmd_result)
        client.subscribe(cli_to_cloud_sub_top_fog2_d5_cmd_result)
        client.subscribe(cli_to_cloud_sub_top_fog2_d6_cmd_result)


        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message_cloud
            client.loop_stop()  # stop the loop

    elif(thread_type=="Publish_Cloud"):
        cloud_pub_connect_message("fog1", "connect")
        cloud_pub_connect_message("fog2", "connect")

        time.sleep(3)
        input("Press Enter to continue...\n")
        print("Publish: arm under topic:", cli_to_cloud_pub_top_fog1_cmd)
        publish_to_cloud(cli_to_cloud_pub_top_fog1_cmd, "arm")
        publish_to_cloud(cli_to_cloud_pub_top_fog2_cmd, "arm")
        input("Press Enter to continue...\n")
        time.sleep(3)
        publish_to_cloud(cli_to_cloud_pub_top_fog1_cmd, "takeoff")
        publish_to_cloud(cli_to_cloud_pub_top_fog2_cmd, "takeoff")
        input("Press Enter to continue...\n")
        time.sleep(3)
        publish_to_cloud(cli_to_cloud_pub_top_fog1_cmd, "land")
        publish_to_cloud(cli_to_cloud_pub_top_fog2_cmd, "land")
        input("Press Enter to continue...\n")
        time.sleep(3)
        print("the end")

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



    now = datetime.datetime.utcnow()
    now_local = datetime.datetime.now()
    print(now_local)
    sub_cloud_thread = sub_pub_thread(1, "Subscribe_Cloud")
    pub_cloud_thread = sub_pub_thread(2, "Publish_Cloud")

    sub_cloud_thread.start()
    pub_cloud_thread.start()

    sub_cloud_thread.join()
    pub_cloud_thread.join()


#endregion

# region Code start
if __name__ == '__main__':
    main()
# endregion

