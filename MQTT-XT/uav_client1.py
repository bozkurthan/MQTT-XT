#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
vehicle_state.py: 
Demonstrates how to get and set vehicle state and parameter information, 
and how to observe vehicle attribute (state) changes.
Full documentation is provided at http://python.dronekit.io/examples/vehicle_state.html
"""
from __future__ import print_function
from dronekit import connect, VehicleMode
import threading

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish

import time


connection_string = "127.0.0.1:14550"


client_ID = "end_user"

test_packet_length = 5

broker_cloud_address = "192.168.1.41" # bu clientta etki etmıyor
broker_cloud_port = 1884

cloud_connect=True

client_pub_topic_connection = "drone1/state"

print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

vehicle.wait_ready('autopilot_version')

# Get all vehicle attributes (state)



print(" Global Location: %s" % vehicle.location.global_frame)
print(" Battery: %s" % vehicle.battery)
print(" Mode: %s" % vehicle.mode.name)  # settable
print(" Groundspeed: %s" % vehicle.groundspeed)
print(" System status: %s" % vehicle.system_status.state)
print(" Heading: %s" % vehicle.heading)
print(" Armed: %s" % vehicle.armed)  # settable
print(" Is Armable?: %s" % vehicle.is_armable)
print(" Attitude: %s" % vehicle.attitude)




def client_pub ():
    print("This client will be run for only publishing. \n ")
    #client = mqtt.Client(client_ID)  # create new instance
    global cloud_connect
    global broker_cloud_address
    global broker_cloud_port
    global client_pub_topic_connection
    print(cloud_connect)
    while (cloud_connect==True):
            publish_message = str(vehicle.location.global_frame)
            print(publish_message)
            publish.single(client_pub_topic_connection+"/location", publish_message, 2, False, broker_cloud_address, broker_cloud_port)
            time.sleep(1)
            publish_message = str(vehicle.battery)
            publish.single(client_pub_topic_connection+"/battery", publish_message, 2, False, broker_cloud_address, broker_cloud_port)
            time.sleep(1)

client_pub()
# Get Vehicle Home location - will be `None` until first set by autopilot
#while not vehicle.home_location:
#    cmds = vehicle.commands
#    cmds.download()
#    cmds.wait_ready()
#    if not vehicle.home_location:
#        print(" Waiting for home location ...")
# We have a home location, so print it!        
#print("\n Home location: %s" % vehicle.home_location)

# Set vehicle home_location, mode, and armed attributes (the only settable attributes)

#print("\nSet new home location")
# Home location must be within 50km of EKF home location (or setting will fail silently)
# In this case, just set value to current location with an easily recognisable altitude (222)
#my_location_alt = vehicle.location.global_frame
#my_location_alt.alt = 222.0
#vehicle.home_location = my_location_alt
#print(" New Home Location (from attribute - altitude should be 222): %s" % vehicle.home_location)

# Confirm current value on vehicle by re-downloading commands
#cmds = vehicle.commands
#cmds.download()
#cmds.wait_ready()
#print(" New Home Location (from vehicle - altitude should be 222): %s" % vehicle.home_location)

#print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name)
#vehicle.mode = VehicleMode("GUIDED")

# Check that vehicle is armable
#while not vehicle.is_armable:
#    print(" Waiting for vehicle to initialise...")
#    time.sleep(1)


## Reset variables to sensible values.
#print("\nReset vehicle attributes/parameters and exit")
#vehicle.mode = VehicleMode("STABILIZE")
#vehicle.armed = False


# Close vehicle object before exiting script
#print("\nClose vehicle object")
#vehicle.close()


print("Completed")
