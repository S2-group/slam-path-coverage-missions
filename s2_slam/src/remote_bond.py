#!/usr/bin/env python3
import rospy, time
import roslaunch
import sys, select, os
import pyrosbag
from bondpy import bondpy

def bondToRobot():
    #set id to send over topic
    id = "read_resources"
    #send id over topic
    bond = bondpy.Bond("bond_resources", id)
    #start bond
    bond.start()

    #check if bond is formed
    if not bond.wait_until_formed(rospy.Duration(1.0)):
        exit()

    #pyrosbag python library handling rosbag playback
    with pyrosbag.BagPlayer(sys.argv[1]) as mission:
        mission.play()
        while mission.is_running:
            pass
            #wait for mission to end
    #break bond when mission is over
    bond.break_bond()

if __name__=='__main__':
    #initialize node
    rospy.init_node('bond_remote')
    bondToRobot()
    #kills remote bond node after execution
    os.system("rosnode kill /remote_bond")
