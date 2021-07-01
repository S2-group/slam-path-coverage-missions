#!/usr/bin/env python3
import rospy, time
import roslaunch
import sys, select, os
import pyrosbag
from bondpy import bondpy

def launchResourceMeter():
    #sets parameters to launch resource meter Node
    package = 's2_slam'
    executable = 'resource_meter.py'
    node = roslaunch.core.Node(package, executable)

    #launches the node
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)
    return process


def bondToRemote():
    #sets id to send over topic
    id = "read_resources"
    #sends id over topic
    bond = bondpy.Bond("bond_resources", id)
    #set connection timeout related to bug where wait_until_formed returns true
    #if the connect_timeout variable is smaller than the time value fed into
    #the wait_until_broken function
    bond.set_connect_timeout(rospy.Duration(60))
    #start bond
    bond.start()
    #wait 60 seconds for bond to form
    if not bond.wait_until_formed(rospy.Duration(60)):
        raise Exception('Bond could not be formed')
        exit()
    #sets resource meter as a variable named process
    process = launchResourceMeter()
    #waits until bond is broken
    bond.wait_until_broken()
    #stops resource meter
    process.stop()


if __name__=='__main__':
    #initialize node
    rospy.init_node('bond_robot')
    bondToRemote()
