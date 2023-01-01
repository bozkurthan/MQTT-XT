# region imports
from __future__ import print_function
import threading
import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
#endregion


# region MQTT connection Variables
client_ID1 = "activator_clientab"
client_ID2 = "activator_clientac"

broker_cloud_address = "192.168.1.45"
broker_cloud_port = 1885
broker_fog_address = "192.168.1.45"
broker_fog_port = 1883
fog_number="fog1"

# endregion


#region Topics

#region Topics to Publish

#topics pub to cloud

#Connectivity
cli_to_cloud_pub_top_d1_reach=fog_number+"/drone1/reachable"
cli_to_cloud_pub_top_d2_reach=fog_number+"/drone2/reachable"
cli_to_cloud_pub_top_d3_reach=fog_number+"/drone3/reachable"


#Drone states
cli_to_cloud_pub_top_d1_state=fog_number+"/drone1/state/#"
cli_to_cloud_pub_top_d2_state=fog_number+"/drone2/state/#"
cli_to_cloud_pub_top_d3_state=fog_number+"/drone3/state/#"


cli_to_cloud_pub_top_qdos=fog_number+"/qods/"

#Command Results
cli_to_cloud_pub_top_d1_cmd_result=fog_number+"/drone1/commands_result"
cli_to_cloud_pub_top_d2_cmd_result=fog_number+"/drone2/commands_result"
cli_to_cloud_pub_top_d3_cmd_result=fog_number+"/drone3/commands_result"



#topics pub to own server
cli_to_fog_pub_top_d1_cmd="drone1/commands"
cli_to_fog_pub_top_d2_cmd="drone2/commands"
cli_to_fog_pub_top_d3_cmd="drone3/commands"


#endregion

#region Topics to Subscribe

#topics sub to fog broker
cli_to_fog_sub_top_d1_state = "drone1/state/#"
cli_to_fog_sub_top_d2_state = "drone2/state/#"
cli_to_fog_sub_top_d3_state = "drone3/state/#"

cli_to_fog_sub_top_d1_command_result = "drone1/commands_result/#"
cli_to_fog_sub_top_d2_command_result = "drone2/commands_result/#"
cli_to_fog_sub_top_d3_command_result = "drone3/commands_result/#"


#topics sub to cloud

#Connectivity
cli_to_cloud_sub_top_connect = "init/" + fog_number

#Commands
cli_to_cloud_sub_top_d1_cmd = fog_number + "/drone1/commands"
cli_to_cloud_sub_top_d2_cmd = fog_number + "/drone2/commands"
cli_to_cloud_sub_top_d3_cmd = fog_number + "/drone3/commands"
cli_to_cloud_sub_top_cmd_all = fog_number + "/commands_all"


#endregion

#endregion

# region qdos parameters
drone1_battery =0
drone2_battery =0
drone3_battery =0

drone1_groundspeed = 0
drone2_groundspeed = 0
drone3_groundspeed = 0

qdos_array = ["drone1", "drone2","drone3"]

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
        publish_to_fog(cli_to_fog_pub_top_d1_cmd, message)
        time.sleep(1)
        publish_to_fog(cli_to_fog_pub_top_d2_cmd, message)
        time.sleep(1)
        publish_to_fog(cli_to_fog_pub_top_d3_cmd, message)
        time.sleep(1)
    elif(topic==cli_to_cloud_sub_top_d1_cmd):
        publish_to_fog(cli_to_fog_pub_top_d1_cmd,message)
    elif(topic==cli_to_cloud_sub_top_d2_cmd):
        publish_to_fog(cli_to_fog_pub_top_d2_cmd,message)
    elif(topic==cli_to_cloud_sub_top_d3_cmd):
        publish_to_fog(cli_to_fog_pub_top_d3_cmd,message)


#calculate qdos based on battery and groundspeed
def qdos_calculate():
    global drone1_battery
    global drone2_battery
    global drone3_battery
    global drone1_groundspeed
    global drone2_groundspeed
    global drone3_groundspeed

    if(float(drone1_battery)>float(drone2_battery)):
        publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone1,drone2")
    elif(float(drone1_battery)<float(drone2_battery)):
        publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone2,drone1")
    elif(float(drone1_battery)==float(drone2_battery)):
        if(float(drone1_groundspeed)>float(drone2_groundspeed)):
            publish_to_cloud(cli_to_cloud_pub_top_qdos,"drone1,drone2")
        else:
            publish_to_cloud(cli_to_cloud_pub_top_qdos, "drone2,drone1")

#process fog messages (this includes to publish state of drones, qdos values and drone reacheability
def process_sub_message_fog(message,topic):
    #print("Fog Topic:"+topic,",Message:"+message)
    global drone1_battery
    global drone2_battery
    global drone1_groundspeed
    global drone2_groundspeed
    global qdos_array

    #only publish if cloud is connected
    if(cloud_connect):

        # region drone1 states
        if(topic=="drone1/state/location" or topic=="drone1/state/mode" or topic=="drone1/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d1_reach, "true")
        if(topic=="drone1/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d1_reach, "true")
            drone1_battery=message
            qdos_calculate()
        if (topic == "drone1/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d1_reach, "true")
            drone1_groundspeed = message
            qdos_calculate()

        #endregion

        #region drone2 states
        if(topic=="drone2/state/location" or topic=="drone2/state/mode" or topic=="drone2/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d2_reach, "true")
        if(topic=="drone2/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d2_reach, "true")
            drone2_battery=message
            qdos_calculate()
        if (topic == "drone2/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d2_reach, "true")
            drone2_groundspeed = message
            qdos_calculate()
        #endregion

        # region drone3 states
        if(topic=="drone3/state/location" or topic=="drone3/state/mode" or topic=="drone3/state/heading" ):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d3_reach, "true")
        if(topic=="drone3/state/battery"):
            publish_to_cloud(fog_number+"/"+topic,message)
            publish_to_cloud(cli_to_cloud_pub_top_d3_reach, "true")
        if (topic == "drone3/state/groundspeed"):
            publish_to_cloud(fog_number + "/" + topic, message)
            publish_to_cloud(cli_to_cloud_pub_top_d3_reach, "true")


        #region command results
        if (topic.startswith("drone1/commands_result")):
            publish_to_cloud(fog_number + "/" + topic, message)
        if (topic.startswith("drone2/commands_result")):
            publish_to_cloud(fog_number+"/"+topic,message)
        if (topic.startswith("drone3/commands_result")):
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
        client.subscribe(cli_to_fog_sub_top_d1_state)
        client.subscribe(cli_to_fog_sub_top_d2_state)
        client.subscribe(cli_to_fog_sub_top_d3_state)
        client.subscribe(cli_to_fog_sub_top_d1_command_result)
        client.subscribe(cli_to_fog_sub_top_d2_command_result)
        client.subscribe(cli_to_fog_sub_top_d3_command_result)
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
        client.subscribe(cli_to_cloud_sub_top_d1_cmd)
        client.subscribe(cli_to_cloud_sub_top_d2_cmd)
        client.subscribe(cli_to_cloud_sub_top_d3_cmd)
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







