#!/usr/bin/env python3
import rospy, time
import roslaunch
import sys, select, os
import pyrosbag
from bondpy import bondpy

def launchResourceMeter():
    package = 's2_slam'
    executable = 'resource_meter.py'
    node = roslaunch.core.Node(package, executable)

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()
    process = launch.launch(node)
    return process


def bondToRemote():
    id = "read_resources"
    bond = bondpy.Bond("bond_resources", id)
    bond.set_connect_timeout(rospy.Duration(60))
    bond.start()
    if not bond.wait_until_formed(rospy.Duration(60)):
        raise Exception('Bond could not be formed')
        exit()
    process = launchResourceMeter()
    bond.wait_until_broken()
    process.stop()


if __name__=='__main__':
    rospy.init_node('bond_robot')
    bondToRemote()
