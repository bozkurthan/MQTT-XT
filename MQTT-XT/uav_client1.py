# region imports
from __future__ import print_function
from dronekit import connect, VehicleMode
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
fog_broker_adress = "192.168.1.42"  # bu clientta etki etmıyor
fog_broker_port = 1884
# endregion


#region Topics

#region Topics to Publish
client_pub_topic_state = "drone1/state"
#endregion

#region Topics to Subscribe
client_sub_topic_command = "drone1/commands"
#endregion
#endregion

# region Function definitions

#Drone connection
def connect_to_drone():
    print("\nConnecting to vehicle on: %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)

    # wait for ready signal
    vehicle.wait_ready('autopilot_version')

    return vehicle

def publish_to_fog(publish_topic,publish_message):
    #Announcement for function
    #client = mqtt.Client(client_ID)  # create new instance
    #print(publish_message)
    publish.single(publish_topic, publish_message, 2, False, fog_broker_adress, fog_broker_port)
    time.sleep(0.2)


def process(sub_message):
    print("Sub message:", sub_message)
    if (sub_message[0] == "takeoff"):
        print("helloWorld1: "+ sub_message)
        #publish.single(client_pub_topic_drone1_state+"/location", sub_message, 1, False, broker_cloud_address, broker_cloud_port)
        vehicle.simple_takeoff("20")
    if (sub_message[0] == "B"):
        print("helloWorld2: " + sub_message)
        #publish.single(client_pub_topic_drone1_state+"/battery", sub_message, 1, False, broker_cloud_address, broker_cloud_port)

def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    process(sub_message)

def func_sub_pub(thread_type):
    if (thread_type == "Publish_Fog"):
        print("This thread will publish drone state to FoG. \n ")
        # start drone connection
        vehicle = connect_to_drone()
        while (1):
            publish_to_fog(client_pub_topic_state + "/location",
                           "lat:" + str(vehicle.location.global_frame.lat) + " lon:" + str(
                               vehicle.location.global_frame.lon) + " alt:" + str(vehicle.location.global_frame.alt))
            publish_to_fog(client_pub_topic_state + "/battery", str(vehicle.battery.level))
            publish_to_fog(client_pub_topic_state + "/groundspeed", str(vehicle.groundspeed))
            publish_to_fog(client_pub_topic_state + "/mode", str(vehicle.mode.name))
            publish_to_fog(client_pub_topic_state + "/heading", str(vehicle.heading))

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


########## MAIN CLASS
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





# pragma Vehicle attributes to receive
# Get all vehicle attributes (state)

# print(" Global Location: %s" % vehicle.location.global_frame)s
# print(" Battery: %s" % vehicle.battery)
# print(" Mode: %s" % vehicle.mode.name)  # settable
# print(" Groundspeed: %s" % vehicle.groundspeed)
# print(" System status: %s" % vehicle.system_status.state)
# print(" Heading: %s" % vehicle.heading)
# print(" Armed: %s" % vehicle.armed)  # settable
# print(" Is Armable?: %s" % vehicle.is_armable)
# print(" Attitude: %s" % vehicle.attitude)




# Get Vehicle Home location - will be `None` until first set by autopilot
# while not vehicle.home_location:
#    cmds = vehicle.commands
#    cmds.download()
#    cmds.wait_ready()
#    if not vehicle.home_location:
#        print(" Waiting for home location ...")
# We have a home location, so print it!        
# print("\n Home location: %s" % vehicle.home_location)

# Set vehicle home_location, mode, and armed attributes (the only settable attributes)

# print("\nSet new home location")
# Home location must be within 50km of EKF home location (or setting will fail silently)
# In this case, just set value to current location with an easily recognisable altitude (222)
# my_location_alt = vehicle.location.global_frame
# my_location_alt.alt = 222.0
# vehicle.home_location = my_location_alt
# print(" New Home Location (from attribute - altitude should be 222): %s" % vehicle.home_location)

# Confirm current value on vehicle by re-downloading commands
# cmds = vehicle.commands
# cmds.download()
# cmds.wait_ready()
# print(" New Home Location (from vehicle - altitude should be 222): %s" % vehicle.home_location)

# print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name)
# vehicle.mode = VehicleMode("GUIDED")

# Check that vehicle is armable
# while not vehicle.is_armable:
#    print(" Waiting for vehicle to initialise...")
#    time.sleep(1)


## Reset variables to sensible values.
# print("\nReset vehicle attributes/parameters and exit")
# vehicle.mode = VehicleMode("STABILIZE")
# vehicle.armed = False



