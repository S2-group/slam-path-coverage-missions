#!/usr/bin/env python3
import rospy, time
import roslaunch
import sys, select, os
import pyrosbag
from bondpy import bondpy

def bondToRobot():
    id = "read_resources"
    bond = bondpy.Bond("bond_resources", id)
    bond.start()

    if not bond.wait_until_formed(rospy.Duration(1.0)):
        exit()

    with pyrosbag.BagPlayer(sys.argv[1]) as mission:
        mission.play()
        while mission.is_running:
            pass
            #wait for mission to end
    bond.break_bond()

if __name__=='__main__':
    rospy.init_node('bond_remote')
    bondToRobot()
    os.system("rosnode kill /remote_bond")
