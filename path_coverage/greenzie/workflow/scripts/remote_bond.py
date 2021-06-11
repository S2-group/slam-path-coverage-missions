#!/usr/bin/env python3
import rospy
from bondpy import bondpy
import roslaunch

# Launches rosbag record and dumpcap
def launchProfilers():
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/ubuntu/greenzie_catkin_ws/src/workflow/launch/profilers.launch"])
    launch.start()

def setBond():
    id = "metric_bond"
    bond = bondpy.Bond("metric_bond", id)    
    bond.set_connect_timeout(rospy.Duration(60.0))
    bond.start()

    if not bond.wait_until_formed(rospy.Duration(60.0)):
        raise Exception('Bond could not be formed')

    print("remote bonded")
    launchProfilers()

    bond.wait_until_broken()

if __name__ == "__main__":
    rospy.init_node('remote_bond_node')
    setBond()
