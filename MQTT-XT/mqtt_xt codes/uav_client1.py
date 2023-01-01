# region imports
from __future__ import print_function

import math
import threading
import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
import asyncio
from mavsdk import System
#endregion


# region UAV variables to connect
connection_string = "127.0.0.1:14550"
global vehicle
#endregion

# region MQTT connection Variables
client_ID = "uav_clientx"
fog_broker_adress = "192.168.1.45"  # bu clientta etki etmıyor
fog_broker_port = 1883
# endregion


#region Topics

#region Topics to Publish
client_pub_topic_state = "drone1/state"
client_pub_topic_command_result= "drone1/commands_result"
#endregion

#region Topics to Subscribe
client_sub_topic_command = "drone1/commands"
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
    time.sleep(0.1)




def process(sub_message):
    print("Sub message:", sub_message)
    if (sub_message == "takeoff"):
        print("Takeoff command received.")
        # try to start command
        #TAKEOFF COMMAND
        #if takeoff success
        print("Publishing:",client_pub_topic_command_result + "/takeoff")
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
    elif (sub_message == "offboard,70"):
        print("offboard,70 command received.")
        # try to start command
        #MODE CHANGE COMMAND
        #if change success
        print("Offboard Change success.")
        publish_to_fog(client_pub_topic_command_result + "/mode_change", "Success")
        #else
        #print("Mode Change Failed.")
        #publish_to_fog(client_pub_topic_command_result + "/mode_change", "Failed")
    elif (sub_message == "arm"):
        print("Arm command received.")
        # try to start command
        #MISSION COMMAND
        #if mission success
        print("Publishing:",client_pub_topic_command_result + "/arm")
        publish_to_fog(client_pub_topic_command_result + "/arm", "Success")
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

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        #print(f"Battery: {battery.remaining_percent}")
        publish_to_fog(client_pub_topic_state + "/battery", str(battery.remaining_percent))
        await asyncio.sleep(1)


async def print_gs_info(drone):
    async for velocity in drone.telemetry.velocity_ned():
        speed = math.sqrt(velocity.east_m_s * velocity.east_m_s + velocity.north_m_s * velocity.north_m_s)
        #print(f"GS info:"+ str(speed))
        publish_to_fog(client_pub_topic_state + "/groundspeed", str(speed))
        await asyncio.sleep(1)

async def print_heading_info(drone):
    async for heading in drone.telemetry.raw_gps():
        gps_heading = heading.heading_uncertainty_deg
        #print(f"heading {gps_heading}")
        publish_to_fog(client_pub_topic_state + "/heading", str(gps_heading))
        await asyncio.sleep(1)

async def print_flightmode_info(drone):
    async for flight_mode in drone.telemetry.flight_mode():
        #print("FlightMode:", flight_mode)
        publish_to_fog(client_pub_topic_state + "/mode", str(flight_mode))
        await asyncio.sleep(1)


async def print_position(drone):
    async for position in drone.telemetry.position():
        #print(position)
        publish_to_fog(client_pub_topic_state + "/location", str(position))
        await asyncio.sleep(1)


async def run():
    # Init the drone
    global drone
    drone = System()
    await drone.connect(system_address="udp://:14540")
    # Start the tasks
    asyncio.ensure_future(print_battery(drone))
    asyncio.ensure_future(print_position(drone))
    asyncio.ensure_future(print_flightmode_info(drone))
    asyncio.ensure_future(print_gs_info(drone))
    asyncio.ensure_future(print_heading_info(drone))

def func_sub_pub(thread_type):
    if (thread_type == "Publish_Fog"):
        print("This thread will publish drone state to FoG. \n ")

        loop = asyncio.new_event_loop()
        try:
            loop.create_task(run())
            loop.run_forever()
        finally:
            loop.stop()
            loop.close()



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



