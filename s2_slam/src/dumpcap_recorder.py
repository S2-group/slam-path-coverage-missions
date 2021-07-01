#!/usr/bin/env python3
import rospy
import os
import time

def recordPackets():
    now = str(time.time())
    #command to run dumpcap and append timecode to output file name
    command = 'dumpcap -f "host turtlebot-ip" -w ~/Robot_Data/output-' + now + '.pcap'
    #command is run
    os.system(command)

if __name__ == "__main__":
    #initializes node
    rospy.init_node("dumpcap_recorder")
    recordPackets()
