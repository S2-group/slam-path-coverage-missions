#!/usr/bin/env python

import rospy
import os
import actionlib
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from boustrophedon_msgs.msg import PlanMowingPathAction
from geometry_msgs.msg import PolygonStamped
from boustrophedon_msgs.msg import PlanMowingPathGoal

from actionlib_msgs.msg import GoalStatus


def parseValues(axis):  
    points = []
    
    try:
        with open("/home/ubuntu/greenzie_catkin_ws/src/maps/arena/" + axis + "_coordinates.txt") as file_reader:
            line = file_reader.readline()
            while line != '':
                points.append(float(line.rstrip("\n")))
                line = file_reader.readline()
    except:
        rospy.logerr("Could not process the file - " + axis + "_coordinates.txt")

    return points

if __name__ == '__main__':
    rospy.init_node('boustrophedon_planner_client_node')

    x_points = parseValues("x")
    y_points = parseValues("y")

    if(len(x_points) != len(y_points)):
        raise Exception("Incomplete Coordinates")

    client = actionlib.SimpleActionClient('plan_path', PlanMowingPathAction)

    rospy.loginfo("Waiting for action server to start.")
    client.wait_for_server()

    rospy.loginfo("Action server started, sending goal.")

    goal = PlanMowingPathGoal()

    property = PolygonStamped()

    for i in range(len(x_points)):
        point = Point()
        property.header.frame_id = "map"
        point.z = 0
        point.x = x_points[i]
        point.y = y_points[i]
        property.polygon.points.append(point)

    robot_position = PoseStamped()
    robot_position.header.frame_id = "map"
    robot_position.pose.orientation.x = 0
    robot_position.pose.orientation.y = 0
    robot_position.pose.orientation.z = 0
    robot_position.pose.orientation.w = 1
    robot_position.pose.position.x = -0.19
    robot_position.pose.position.y = 0.64
    robot_position.pose.position.z = 0

    goal.property = property
    goal.robot_position = robot_position
    client.send_goal(goal)

    finished_before_timeout = client.wait_for_result(rospy.Duration(30.0))

    if(finished_before_timeout):
        rospy.loginfo("Action finished")
    else:
        rospy.loginfo("Action did not finish before the time out.")



