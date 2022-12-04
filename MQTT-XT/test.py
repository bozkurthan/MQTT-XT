# region imports
from __future__ import print_function
import threading
import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
#endregion


# region UAV variables to connect
connection_string = "127.0.0.1:14550"
global vehicle
#endregion

# region MQTT connection Variables
client_ID = "uav_client1"
fog_broker_adress = "127.0.0.1"  # bu clientta etki etmıyor
fog_broker_port = 1884
# endregion


#region Topics

#region Topics to Publish
client_pub_topic_state = "drone2/state"
client_pub_topic_command_result= "drone2/commands_result"
#endregion

#region Topics to Subscribe
client_sub_topic_command = "drone2/commands"
#endregion
#endregion

# region Function definitions

#Drone connection
def connect_to_drone():
    print("\nConnecting to vehicle on: %s" % connection_string)
    #vehicle = connect(connection_string, wait_ready=True)

    # wait for ready signal
    #vehicle.wait_ready('autopilot_version')

    #return vehicle

def publish_to_fog(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, fog_broker_adress, fog_broker_port)
    #time.sleep(0.2)


def process(sub_message):
    print("Sub message:", sub_message)
    if (sub_message == "takeoff"):
        print("Takeoff command received.")
        # try to start command
        #TAKEOFF COMMAND
        #if takeoff success
        print("Takeoff success.")
        publish_to_fog(client_pub_topic_command_result + "/takeoff", "Success")
        #else
        #print("Takeoff Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/takeoff", "Failed")
        #vehicle.simple_takeoff("20")
    elif (sub_message == "land"):
        print("Land command received.")
        # try to start command
        #LAND COMMAND
        #if land success
        print("Land success.")
        publish_to_fog(client_pub_topic_command_result + "/land", "Success")
        #else
        #print("Land Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/land", "Failed")
    elif (sub_message == "goto"):
        print("Goto command received.")
        # try to start command
        #GOTO COMMAND
        #if goto success
        print("GoTo success.")
        publish_to_fog(client_pub_topic_command_result + "/goto", "Success")
        #else
        #print("Goto Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/goto", "Failed")
    elif (sub_message == "mode_change"):
        print("Mode change command received.")
        # try to start command
        #MODE CHANGE COMMAND
        #if change success
        print("Mode Change success.")
        publish_to_fog(client_pub_topic_command_result + "/mode_change", "Success")
        #else
        #print("Mode Change Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/mode_change", "Failed")
    elif (sub_message == "mission"):
        print("Mission command received.")
        # try to start command
        #MISSION COMMAND
        #if mission success
        print("Mission start success.")
        publish_to_fog(client_pub_topic_command_result + "/mission", "Success")
        #else
        #print("Mission start Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/mission", "Failed")
    else:
        print("Unknown command received.")
        # try to start command
        publish_to_fog(client_pub_topic_command_result + "/"+sub_message, "Unknown")

def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    process(sub_message)

def func_sub_pub(thread_type):
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

    pub_fog_thread = sub_pub_thread(1, "Publish_Fog")

    sub_fog_thread = sub_pub_thread(2, "Subscribe_Fog")

    pub_fog_thread.start()
    sub_fog_thread.start()

    pub_fog_thread.join()
    sub_fog_thread.join()


    # Close vehicle object before exiting script
    print("\nClose vehicle object")
    #vehicle.close()

#endregion

# region Code start
if __name__ == '__main__':
    main()
# endregion



