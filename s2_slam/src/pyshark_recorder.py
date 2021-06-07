#!/usr/bin/env python3
import pyshark
import rospy
import subprocess
import os
import time

def recordPackets():
    now = str(time.time())
    command = 'dumpcap -f "host turtlebot-ip" -w ~/Robot_Data/output-' + now + '.pcap'
    os.system(command)

if __name__ == "__main__":
    rospy.init_node("pyshark_recorder")
    recordPackets()
