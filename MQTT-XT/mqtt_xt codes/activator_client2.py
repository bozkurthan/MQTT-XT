# region imports
from __future__ import print_function
import threading
import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
#endregion


# region MQTT connection Variables
client_ID1 = "activator_clientb"
client_ID2 = "activator_clientc"

broker_cloud_address = "127.0.0.1"
broker_cloud_port = 1885
broker_fog_address = "192.168.1.45"
broker_fog_port = 1884
fog_number="fog2"

# endregion


#region Topics

#region Topics to Publish

#topics pub to cloud

#Connectivity
cli_to_cloud_pub_top_d4_reach=fog_number+"/drone4/reachable"
cli_to_cloud_pub_top_d5_reach=fog_number+"/drone5/reachable"
cli_to_cloud_pub_top_d6_reach=fog_number+"/drone6/reachable"


#Drone states
cli_to_cloud_pub_top_d4_state=fog_number+"/drone4/state/#"
cli_to_cloud_pub_top_d5_state=fog_number+"/drone5/state/#"
cli_to_cloud_pub_top_d6_state=fog_number+"/drone6/state/#"


cli_to_cloud_pub_top_qdos=fog_number+"/qods/"

#Command Results
cli_to_cloud_pub_top_d4_cmd_result=fog_number+"/drone4/commands_result"
cli_to_cloud_pub_top_d5_cmd_result=fog_number+"/drone5/commands_result"
cli_to_cloud_pub_top_d6_cmd_result=fog_number+"/drone6/commands_result"



#topics pub to own server
cli_to_fog_pub_top_d4_cmd="drone4/commands"
cli_to_fog_pub_top_d5_cmd="drone5/commands"
cli_to_fog_pub_top_d6_cmd="drone6/commands"


#endregion

#region Topics to Subscribe

#topics sub to fog broker
cli_to_fog_sub_top_d4_state = "drone4/state/#"
cli_to_fog_sub_top_d5_state = "drone5/state/#"
cli_to_fog_sub_top_d6_state = "drone6/state/#"

cli_to_fog_sub_top_d4_command_result = "drone4/commands_result/#"
cli_to_fog_sub_top_d5_command_result = "drone5/commands_result/#"
cli_to_fog_sub_top_d6_command_result = "drone6/commands_result/#"


#topics sub to cloud

#Connectivity
cli_to_cloud_sub_top_connect = "init/" + fog_number

#Commands
cli_to_cloud_sub_top_d4_cmd = fog_number + "/drone4/commands"
cli_to_cloud_sub_top_d5_cmd = fog_number + "/drone5/commands"
cli_to_cloud_sub_top_d6_cmd = fog_number + "/drone6/commands"
cli_to_cloud_sub_top_cmd_all = fog_number + "/commands_all"


#endregion

#endregion

# region qdos parameters
drone4_battery =0
drone5_battery =0
drone6_battery =0

drone4_groundspeed = 0
drone5_groundspeed = 0
drone6_groundspeed = 0

qdos_array = ["drone4", "drone5","drone6"]

# endregion

# region Function definitions

cloud_connect=True

# publish message to fog function
def publish_to_fog(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, broker_fog_address, broker_fog_port)

# publish message to cloud function
def publish_to_cloud(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, broker_cloud_address, broker_cloud_port)



def process_sub_message_cloud(message,topic):
    print("Cloud Topic:"+topic,",Message:"+message)

    if(message=="connect"):
        print("Connect_message_received:", message)
    if(topic==cli_to_cloud_sub_top_cmd_all):
        print("Command received, under", topic, message)
        publish_to_fog(cli_to_fog_pub_top_d4_cmd, message)
        time.sleep(1)
        publish_to_fog(cli_to_fog_pub_top_d5_cmd, message)
        time.sleep(1)
        publish_to_fog(cli_to_fog_pub_top_d6_cmd, message)
        time.sleep(1)
    elif(topic==cli_to_cloud_sub_top_d4_cmd):
        publish_to_fog(cli_to_fog_pub_top_d4_cmd,message)
    elif(topic==cli_to_cloud_sub_top_d5_cmd):
        publish_to_fog(cli_to_fog_pub_top_d5_cmd,message)
    elif(topic==cli_to_cloud_sub_top_d6_cmd):
        publish_to_fog(cli_to_fog_pub_top_d6_cmd,message)


#calculate qdos based on battery and groundspeed
def qdos_calculate():
    global drone4_battery
    global drone5_battery
    global drone6_battery
    global drone4_groundspeed
    global drone5_groundspeed
    global drone6_groundspeed

    if(float(drone4_battery)>float(drone5_battery)):
        publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone4,drone5")
    elif(float(drone4_battery)<float(drone5_battery)):
        publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone5,drone4")
    elif(float(drone4_battery)==float(drone5_battery)):
        if(float(drone4_groundspeed)>float(drone5_groundspeed)):
            publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone4,drone5")
        else:
            publish_to_cloud(cli_to_cloud_pub_top_qdos, "drone5,drone4")

#process fog messages (this includes to publish state of drones, qdos values and drone reacheability
def process_sub_message_fog(message,topic):
    #print("Fog Topic:"+topic,",Message:"+message)
    global drone4_battery
    global drone5_battery
    global drone4_groundspeed
    global drone5_groundspeed
    global qdos_array

    #only publish if cloud is connected
    if(cloud_connect):

        # region drone4 states
        if(topic=="drone4/state/location" or topic=="drone4/state/mode" or topic=="drone4/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d4_reach, "true")
        if(topic=="drone4/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d4_reach, "true")
            drone4_battery=message
            qdos_calculate()
        if (topic == "drone4/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d4_reach, "true")
            drone4_groundspeed = message
            qdos_calculate()

        #endregion

        #region drone5 states
        if(topic=="drone5/state/location" or topic=="drone5/state/mode" or topic=="drone5/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d5_reach, "true")
        if(topic=="drone5/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d5_reach, "true")
            drone5_battery=message
            qdos_calculate()
        if (topic == "drone5/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d5_reach, "true")
            drone5_groundspeed = message
            qdos_calculate()
        #endregion

        # region drone6 states
        if(topic=="drone6/state/location" or topic=="drone6/state/mode" or topic=="drone6/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d6_reach, "true")
        if(topic=="drone6/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d6_reach, "true")
        if (topic == "drone6/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d6_reach, "true")



        #region command results
        if (topic.startswith("drone4/commands_result")):
            publish_to_cloud(fog_number + "/" + topic, message)
        if (topic.startswith("drone5/commands_result")):
            publish_to_cloud(fog_number+"/"+topic,message)
        if (topic.startswith("drone6/commands_result")):
            publish_to_cloud(fog_number+"/"+topic,message)
        #endregion


# message function that handle fog messages
def callback_on_message_fog(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))

    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_fog(sub_message,topic)

# message function that handle cloud messages
def callback_on_message_cloud(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    topic = message.topic
    process_sub_message_cloud(sub_message,topic)





def func_sub_pub(thread_type):
    if (thread_type == "Subscribe_Fog"):

        print("This client will subscribe to Fog broker. \n ")
        client = mqtt.Client(client_ID1)  # create new instance
        print("connecting to Broker\n")

        client.connect(broker_fog_address,broker_fog_port)  # connect to broker
        client.subscribe(cli_to_fog_sub_top_d4_state)
        client.subscribe(cli_to_fog_sub_top_d5_state)
        client.subscribe(cli_to_fog_sub_top_d6_state)
        client.subscribe(cli_to_fog_sub_top_d4_command_result)
        client.subscribe(cli_to_fog_sub_top_d5_command_result)
        client.subscribe(cli_to_fog_sub_top_d6_command_result)
        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message_fog
            client.loop_stop()  # stop the loop

    elif (thread_type == "Subscribe_Cloud"):

        print("This client will subscribe to Cloud broker. \n ")
        client = mqtt.Client(client_ID2)  # create new instance
        print("connecting to Cloud\n")

        client.connect(broker_cloud_address,broker_cloud_port)  # connect to broker

        client.subscribe(cli_to_cloud_sub_top_connect)
        client.subscribe(cli_to_cloud_sub_top_d4_cmd)
        client.subscribe(cli_to_cloud_sub_top_d5_cmd)
        client.subscribe(cli_to_cloud_sub_top_d6_cmd)
        client.subscribe(cli_to_cloud_sub_top_cmd_all)
        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message_cloud
            client.loop_stop()  # stop the loop




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

    sub_cloud_thread = sub_pub_thread(1, "Subscribe_Cloud")
    sub_fog_thread = sub_pub_thread(2, "Subscribe_Fog")
    #pub_cloud_thread = sub_pub_thread(3, "Publish_Cloud")
    #pub_fog_thread = sub_pub_thread(4, "Publish_Fog")

    sub_cloud_thread.start()
    sub_fog_thread.start()
    #pub_cloud_thread.start()
    #pub_fog_thread.start()

    sub_cloud_thread.join()
    sub_fog_thread.join()
    #pub_cloud_thread.join()
    #pub_fog_thread.join()

#endregion

# region Code start
if __name__ == '__main__':
    main()
# endregion







