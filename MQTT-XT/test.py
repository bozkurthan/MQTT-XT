import paho.mqtt.client as mqtt #import the client1
import time
from pymavlink import mavutil
import time


# Create the connection
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# https://mavlink.io/en/messages/common.html#MAV_CMD_COMPONENT_ARM_DISARM

# Arm
# master.arducopter_arm() or:


############
def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)
	now_ns = time.time_ns() # Time in nanoseconds
	now_ms = int(now_ns * 1000)
	print(now_ms)
	master.mav.command_long_send(
	master.target_system,
	master.target_component,
	mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
	0,
	1, 0, 0, 0, 0, 0, 0)

	# wait until arming confirmed (can manually check with master.motors_armed())
	print("Waiting for the vehicle to arm")
	#master.motors_armed_wait()
	print('Armed!')

	# Disarm
	# master.arducopter_disarm() or:
	#master.mav.command_long_send(
	#    master.target_system,
	#    master.target_component,
	#    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
	#    0,
	#    0, 0, 0, 0, 0, 0, 0)
	# wait until disarming confirmed
	#master.motors_disarmed_wait()


########################################
broker_address="test.mosquitto.org"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","drone1")
client.subscribe("topic22")


#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","OFF")
time.sleep(44) # wait
client.loop_stop() #stop the loop