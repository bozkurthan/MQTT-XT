import socket
import struct
import time
TCP_IP = '127.0.0.1' 
TCP_PORT = 1883      
BUFFER_SIZE = 1024

hexa_connect_string = "10 24 00 06 4d 51 49 73 64 70 03 02 00 3c 00 16 6d 6f 73 71 70 75 62 7c 38 33 39 31 2d 68 75 6e 63 68 6f 2d 57 53"

hexa_publish_string = "30 18 00 0a 74 65 73 74 5f 74 6f 70 69 63 48 45 4c 4c 4f 20 57 4f 52 4c 44 21" 

hexa_disconnect_string = "e0 00"

byte_array_connect = bytearray.fromhex(hexa_connect_string)
byte_array_pub = bytearray.fromhex(hexa_publish_string)
byte_array_disconnect = bytearray.fromhex(hexa_disconnect_string)

print("Connect array:" + byte_array_connect)
print("Publish array:" + byte_array_pub)
print("Disconnect array:" + byte_array_pub)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(byte_array_connect)
data = s.recv(BUFFER_SIZE)
print( "received data after connect:", data)
print("connected")
#time.sleep(0.5)
s.send(byte_array_pub)
#data = s.recv(BUFFER_SIZE)
print("published")
s.send(byte_array_disconnect)
print("disconnected")

s.close()
