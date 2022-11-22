# -*- coding: utf-8 -*-

import os
import shutil
import time

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import psutil
from numpy import long

# model girdilerini almak için 2D bir dizi oluşturulsu- dolu değerleri bu diziliere alınıp modele verielcek


global sub_message

# pragma CONFIG
client_ID = "end_user"

test_packet_length = 5

broker_cloud = "127.0.0.1" # bu clientta etki etmıyor
sub_broker_port = 1883
client_sub_topic = "test-fog1"

pub_broker_address = "127.0.0.1"
pub_broker_port = 1883
client_pub_topic = "test-cloud"
publish_delay_time = 0
publish_size = 50
client_number = "FOG1"
location_number = "L1"
packet_name=location_number+ "-"+ client_number

dir_name = "data_log1"
log_dir = os.getcwd()
log_dir = log_dir + "/" + dir_name

if os.path.isdir(log_dir):
    print("File exist")
    shutil.rmtree(log_dir, ignore_errors=True)
    log_dir = log_dir + "/"
    os.mkdir(log_dir)
else:
    log_dir = log_dir + "/"
    os.mkdir(log_dir)

##INCOMING MESSAGE TRANSMISSION TIME LOG DEFINITIONS
total_packet_tx_time_L1_C1 = 0
total_packet_tx_time_L1_C2 = 0
total_packet_tx_time_L1_C3 = 0
total_packet_tx_time_L2_C1 = 0
total_packet_tx_time_L2_C2 = 0
total_packet_tx_time_L2_C3 = 0

total_packet_size_L1_C1 = 0
total_packet_size_L1_C2 = 0
total_packet_size_L1_C3 = 0
total_packet_size_L2_C1 = 0
total_packet_size_L2_C2 = 0
total_packet_size_L2_C3 = 0

packet_counter_L1_C1 = 0
packet_counter_L1_C2 = 0
packet_counter_L1_C3 = 0
packet_counter_L2_C1 = 0
packet_counter_L2_C2 = 0
packet_counter_L2_C3 = 0

##MODEL TIME LOG DEFINITIONS
total_model_proc_time_L1_C1 = 0
total_model_proc_time_L1_C2 = 0
total_model_proc_time_L1_C3 = 0
total_model_proc_time_L2_C1 = 0
total_model_proc_time_L2_C2 = 0
total_model_proc_time_L2_C3 = 0

_mpacket_counter_L1_C1 = 0
_mpacket_counter_L1_C2 = 0
_mpacket_counter_L1_C3 = 0
_mpacket_counter_L2_C1 = 0
_mpacket_counter_L2_C2 = 0
_mpacket_counter_L2_C3 = 0

##PUBLISH MESSAGE PROCCESS LOG DEFINITIONS
total_message_proc_time_L1_C1 = 0
total_message_proc_time_L1_C2 = 0
total_message_proc_time_L1_C3 = 0
total_message_proc_time_L2_C1 = 0
total_message_proc_time_L2_C2 = 0
total_message_proc_time_L2_C3 = 0

_outgoing_total_packet_size_L1_C1 = 0
_outgoing_total_packet_size_L1_C2 = 0
_outgoing_total_packet_size_L1_C3 = 0
_outgoing_total_packet_size_L2_C1 = 0
_outgoing_total_packet_size_L2_C2 = 0
_outgoing_total_packet_size_L2_C3 = 0

publog_mpacket_counter_L1_C1 = 0
publog_mpacket_counter_L1_C2 = 0
publog_mpacket_counter_L1_C3 = 0
publog_mpacket_counter_L2_C1 = 0
publog_mpacket_counter_L2_C2 = 0
publog_mpacket_counter_L2_C3 = 0

def write_cpu_mem_values():
    global total_cpu_usage_percent
    global total_memory_usage_percent
    global total_cpu_temp_percent

    global info_packet_counter
    if (info_packet_counter == test_packet_length):
        model_log_file = open(log_dir + "cpu_usage_percentage.txt", "a")
        model_log_file.write(str(total_cpu_usage_percent / test_packet_length) + "\n")
        model_log_file.close()
        model_size_log_file = open(log_dir + "memory_usage_percentage.txt", "a")
        model_size_log_file.write(str(total_memory_usage_percent / test_packet_length) + "\n")
        model_size_log_file.close()
        model_size_log_file = open(log_dir + "cpu_temperature.txt", "a")
        model_size_log_file.write(str(total_memory_usage_percent / test_packet_length) + "\n")
        model_size_log_file.close()
        total_cpu_usage_percent = 0
        total_memory_usage_percent = 0
        total_cpu_temp_percent = 0
        info_packet_counter = 0
        # else:

    file_read_temp = open("/sys/class/thermal/thermal_zone0/temp", "r")
    temp = file_read_temp.readline()

    total_cpu_usage_percent = total_cpu_usage_percent + psutil.cpu_percent()
    total_memory_usage_percent = total_memory_usage_percent + psutil.virtual_memory().percent
    total_cpu_temp_percent = total_cpu_temp_percent + int(temp) / 1000
    info_packet_counter = info_packet_counter + 1


def incoming_data_log_cfg_tx_time(packet_header, end_time, packet_size):
    global packet_counter_L1_C1
    global packet_counter_L1_C2
    global packet_counter_L1_C3
    global packet_counter_L2_C1
    global packet_counter_L2_C2
    global packet_counter_L2_C3

    global total_packet_tx_time_L1_C1
    global total_packet_tx_time_L1_C2
    global total_packet_tx_time_L1_C3
    global total_packet_tx_time_L2_C1
    global total_packet_tx_time_L2_C2
    global total_packet_tx_time_L2_C3

    global total_packet_size_L1_C1
    global total_packet_size_L1_C2
    global total_packet_size_L1_C3
    global total_packet_size_L2_C1
    global total_packet_size_L2_C2
    global total_packet_size_L2_C3

    if "L1-C1" in packet_header:
        if (packet_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C1.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C1/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C1 = 0
            total_packet_tx_time_L1_C1 = 0
            total_packet_size_L1_C1 = 0
        #else:
        total_packet_tx_time_L1_C1 = total_packet_tx_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C1 = total_packet_size_L1_C1 + packet_size
        packet_counter_L1_C1 = packet_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (packet_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C2/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C2/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C2 = 0
            total_packet_tx_time_L1_C2 = 0
            total_packet_size_L1_C2 = 0
        #else:
        total_packet_tx_time_L1_C2 = total_packet_tx_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C2 = total_packet_size_L1_C2 + packet_size
        packet_counter_L1_C2 = packet_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (packet_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C3/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C3/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C3 = 0
            total_packet_tx_time_L1_C3 = 0
            total_packet_size_L1_C3 = 0
       #else:
        total_packet_tx_time_L1_C3 = total_packet_tx_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C3 = total_packet_size_L1_C3 + packet_size
        packet_counter_L1_C3 = packet_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (packet_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C1.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C1/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C1 = 0
            total_packet_tx_time_L2_C1 = 0
            total_packet_size_L2_C1 = 0
       # else:
        total_packet_tx_time_L2_C1 = total_packet_tx_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C1 = total_packet_size_L2_C1 + packet_size
        packet_counter_L2_C1 = packet_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (packet_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C2/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C2/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C2 = 0
            total_packet_tx_time_L2_C2 = 0
            total_packet_size_L2_C2 = 0
        #else:
        total_packet_tx_time_L2_C2 = total_packet_tx_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C2 = total_packet_size_L2_C2 + packet_size
        packet_counter_L2_C2 = packet_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (packet_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C3/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C3/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C3 = 0
            total_packet_tx_time_L2_C3 = 0
            total_packet_size_L2_C3 = 0
        #else:
        total_packet_tx_time_L2_C3 = total_packet_tx_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C3 = total_packet_size_L2_C3 + packet_size
        packet_counter_L2_C3 = packet_counter_L2_C3 + 1
    else:
        print("Problem in data_log_cfg_tx_time")
def data_log_model_time(packet_header, end_time):
    global _mpacket_counter_L1_C1
    global _mpacket_counter_L1_C2
    global _mpacket_counter_L1_C3
    global _mpacket_counter_L2_C1
    global _mpacket_counter_L2_C2
    global _mpacket_counter_L2_C3

    global total_model_proc_time_L1_C1
    global total_model_proc_time_L1_C2
    global total_model_proc_time_L1_C3
    global total_model_proc_time_L2_C1
    global total_model_proc_time_L2_C2
    global total_model_proc_time_L2_C3

    if "L1-C1" in packet_header:
        if (_mpacket_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C1.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C1 = 0
            total_model_proc_time_L1_C1 = 0
        #else:
        total_model_proc_time_L1_C1 = total_model_proc_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C1 = _mpacket_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (_mpacket_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C2/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C2 = 0
            total_model_proc_time_L1_C2 = 0
        #else:
        total_model_proc_time_L1_C2 = total_model_proc_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C2 = _mpacket_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (_mpacket_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C3/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C3 = 0
            total_model_proc_time_L1_C3 = 0
        #else:
        total_model_proc_time_L1_C3 = total_model_proc_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C3 = _mpacket_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (_mpacket_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C1.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C1/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C1 = 0
            total_model_proc_time_L2_C1 = 0
        #else:
        total_model_proc_time_L2_C1 = total_model_proc_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C1 = _mpacket_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (_mpacket_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C2/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C2 = 0
            total_model_proc_time_L2_C2 = 0
        #else:
        total_model_proc_time_L2_C2 = total_model_proc_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C2 = _mpacket_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (_mpacket_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C3/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C3 = 0
            total_model_proc_time_L2_C3 = 0
        #else:
        total_model_proc_time_L2_C3 = total_model_proc_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C3 = _mpacket_counter_L2_C3 + 1
    else:
        print("Problem in data_log_model_time")
def publish_message_log_time(packet_header, end_time,packet_size):
    global publog_mpacket_counter_L1_C1
    global publog_mpacket_counter_L1_C2
    global publog_mpacket_counter_L1_C3
    global publog_mpacket_counter_L2_C1
    global publog_mpacket_counter_L2_C2
    global publog_mpacket_counter_L2_C3

    global total_message_proc_time_L1_C1
    global total_message_proc_time_L1_C2
    global total_message_proc_time_L1_C3
    global total_message_proc_time_L2_C1
    global total_message_proc_time_L2_C2
    global total_message_proc_time_L2_C3

    global _outgoing_total_packet_size_L1_C1
    global _outgoing_total_packet_size_L1_C2
    global _outgoing_total_packet_size_L1_C3
    global _outgoing_total_packet_size_L2_C1
    global _outgoing_total_packet_size_L2_C2
    global _outgoing_total_packet_size_L2_C3

    print(packet_header)

    if "L1-C1" in packet_header:
        if (publog_mpacket_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C1.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C1.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C1 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C1 = 0
            total_message_proc_time_L1_C1 = 0
            _outgoing_total_packet_size_L1_C1 = 0
        total_message_proc_time_L1_C1 = total_message_proc_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C1 = publog_mpacket_counter_L1_C1 + 1
        _outgoing_total_packet_size_L1_C1 = _outgoing_total_packet_size_L1_C1 + packet_size


    elif "L1-C2" in packet_header:
        if (publog_mpacket_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C2.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C2 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C2.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C2 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C2 = 0
            total_message_proc_time_L1_C2 = 0
            _outgoing_total_packet_size_L1_C2 = 0
        total_message_proc_time_L1_C2 = total_message_proc_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C2 = publog_mpacket_counter_L1_C2 + 1
        _outgoing_total_packet_size_L1_C2 = _outgoing_total_packet_size_L1_C2 + packet_size


    elif "L1-C3" in packet_header:
        if (publog_mpacket_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C3.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C3 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C3.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C3 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C3 = 0
            total_message_proc_time_L1_C3 = 0
            _outgoing_total_packet_size_L1_C3 = 0
        total_message_proc_time_L1_C3 = total_message_proc_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C3 = publog_mpacket_counter_L1_C3 + 1
        _outgoing_total_packet_size_L1_C3 = _outgoing_total_packet_size_L1_C3 + packet_size
    elif "L2-C1" in packet_header:
        if (publog_mpacket_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C1.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C1 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C1.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C1 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C1 = 0
            total_message_proc_time_L2_C1 = 0
            _outgoing_total_packet_size_L2_C1 = 0
        total_message_proc_time_L2_C1 = total_message_proc_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C1 = publog_mpacket_counter_L2_C1 + 1
        _outgoing_total_packet_size_L2_C1 = _outgoing_total_packet_size_L2_C1 + packet_size
    elif "L2-C2" in packet_header:
        if (publog_mpacket_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C2.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C2 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C2.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C2 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C2 = 0
            total_message_proc_time_L2_C2 = 0
            _outgoing_total_packet_size_L2_C2 = 0
        total_message_proc_time_L2_C2 = total_message_proc_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C2 = publog_mpacket_counter_L2_C2 + 1
        _outgoing_total_packet_size_L2_C2 = _outgoing_total_packet_size_L2_C2 + packet_size
    elif "L2-C3" in packet_header:
        if (publog_mpacket_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C3.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C3 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C3.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C3 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C3 = 0
            total_message_proc_time_L2_C3 = 0
            _outgoing_total_packet_size_L2_C3 = 0
        total_message_proc_time_L2_C3 = total_message_proc_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C3 = publog_mpacket_counter_L2_C3 + 1
        _outgoing_total_packet_size_L2_C3 = _outgoing_total_packet_size_L2_C3 + packet_size
    else:
        print("Problem in publish_message_log_time")

def data_process_to_pub(sub_message):
    print("Sub message:", sub_message)

    # These code snippet provides that it handles time by incoming messages and saves them to file.
    # After this operation, it prepares new message.

    print("No NaN value, so directly publish.")
    start_time_for_message_log = long(time.time() * 1000)
    time_first, message_time = sub_message.split("[")
    message_time, unused = message_time.split("]")
    unused, time_last = sub_message.split("]")
    incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
    write_cpu_mem_values()
    new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
    publish_message_log_time(time_first, start_time_for_message_log, new_message.__sizeof__())
    publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
    print("Publish NoNaN:", new_message)


def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    data_process_to_pub(sub_message)

def client_sub_pub():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client(client_ID)  # create new instance
    print("connecting to broker")

    client.connect(broker_cloud)  # connect to broker
    client.subscribe(client_sub_topic)
    while (1):
        client.loop_start()  # start the loop
        # attach function to callback
        client.on_message = callback_on_message
        client.loop_stop()  # stop the loop

def client_pub ():
    print("This client will be run for only publishing. \n ")
    client = mqtt.Client(client_ID)  # create new instance


    print("Without model message process")
    i=0
    while (i<publish_size):
        start_time_for_message_log = long(time.time() * 1000)
        data_message1= "37.511"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
        data_message2= "52.87946" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
        data_message3= "NaN"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
        write_cpu_mem_values()
        publish_message = "( (" + location_number + "-" + client_number + "-" + str(i) + ".Paket), (" + str(long(
            time.time() * 1000)) + "), ( ( Data: (Light: " + data_message1 + ", Humidity: " + data_message2 + ", Temperature:" + data_message3 + ") ) )"
        publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)
        publish_message_log_time(packet_name, start_time_for_message_log,publish_message.__sizeof__())
        time.sleep(publish_delay_time)
        print("Publish:", publish_message)
        i = i + 1



#if (_client_will_sub):
#    client_sub_pub()
#else:
#    client_pub()