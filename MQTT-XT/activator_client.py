# region imports
from __future__ import print_function
import threading
import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
#endregion


# region MQTT connection Variables
client_ID = "activator_client"

broker_cloud_address = "test.mosquitto.org"
broker_cloud_port = 1883
broker_fog_address = "127.0.0.1"
broker_fog_port = 1884
fog_number="fog1"

# endregion


#region Topics

#region Topics to Publish

#topics pub to cloud

#Connectivity
client_pub_topic_drone1_reachability=fog_number+"/drone1/reachable"
client_pub_topic_drone2_reachability=fog_number+"/drone2/reachable"

#Drone states
client_pub_topic_drone1_state=fog_number+"/drone1/state"
client_pub_topic_drone2_state=fog_number+"/drone2/state"
client_pub_topic_drone2_state=fog_number+"/qods/"

#Command Results
client_pub_topic_drone1_command_result=fog_number+"/drone1/state"
client_pub_topic_drone2_state=fog_number+"/drone2/state"


#topics pub to own server
client_pub_topic_drone1_commands="drone1/commands"
client_pub_topic_drone2_state="/drone2/commands"

#endregion

#region Topics to Subscribe

#topics sub to fog broker
client_sub_topic_drone1 = "drone1/state/#"
client_sub_topic_drone2 = "drone2/state/#"

#topics sub to cloud

#Connectivity
client_sub_topic_connection = "init/" + fog_number

#Connectivity
client_sub_topic_drone1_commands = fog_number + "drone1/commands"
client_sub_topic_drone2_commands = fog_number + "drone2/commands"

#endregion

#endregion


# region Function definitions


sub_message_type = dict(get_reachability="0", get_info_drone="1", get_commanmd_result="2")

global sub_message

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

def callback_on_message_fog(client, userdata, message):
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


def publish_to_cloud(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, broker_cloud_address, broker_cloud_port)

def publish_to_fog(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, broker_fog_address, broker_fog_port)

def func_sub_pub(thread_type):
    if (thread_type == "Subscribe_Fog"):

        print("This client will subscribe to own broker. \n ")
        client = mqtt.Client(client_ID)  # create new instance
        print("connecting to Broker")

        client.connect(broker_fog_address)  # connect to broker

        client.subscribe(client_sub_topic_drone1)
        client.subscribe(client_sub_topic_drone2)
        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message_fog
            client.loop_stop()  # stop the loop

    if (thread_type == "Publish_Fog"):
        print("This thread will publish drone state to FoG. \n ")
        # start drone connection
        #vehicle = connect_to_drone()
        while (1):
            publish_to_fog(client_pub_topic_state + "/location",
                           "lat:" + "14.23" + " lon:" + "15.23" + " alt:" + "100")
            publish_to_fog(client_pub_topic_state + "/battery", "50")
            publish_to_fog(client_pub_topic_state + "/groundspeed", "20")
            publish_to_fog(client_pub_topic_state + "/mode", "TAKEOFF")
            publish_to_fog(client_pub_topic_state + "/heading", "200")

    if(thread_type=="Subscribe_Fog"):
        print("This client will wait for command. \n ")

        client = mqtt.Client(client_ID)  # create new instance
        print("connecting to Fog")

        client.connect(fog_broker_adress,fog_broker_port)  # connect to broker
        client.subscribe(client_sub_topic_command)

        while (1):
            client.loop_start()  # start the loop
            # attach function to callback
            client.on_message = callback_on_message
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
    pub_cloud_thread = sub_pub_thread(3, "Publish_Cloud")
    pub_fog_thread = sub_pub_thread(4, "Publish_Fog")

    sub_cloud_thread.start()
    sub_fog_thread.start()
    pub_cloud_thread.start()
    pub_fog_thread.start()

    sub_cloud_thread.join()
    sub_fog_thread.join()
    pub_cloud_thread.join()
    pub_fog_thread.join()

#endregion

# region Code start
if __name__ == '__main__':
    main()
# endregion







