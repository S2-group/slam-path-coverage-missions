#!/usr/bin/env python

import rospy
import os
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PointStamped
from math import sqrt

class PathHandler:
    goalCounter = 0
    def __init__(self):
        rospy.loginfo("Waiting for path points")
        rospy.Subscriber("/boustrophedon_server/path_points", PointStamped, self.pathCallback)

    def getStartPoint():
        start = PointStamped()
        start.pose.position.x = -0.19
        start.pose.position.y = 0.64
        return start

    def isGoalNearStart(self, goal):
        if(abs(goal.target_pose.pose.position.x - self.start.pose.position.x) < 0.1 and abs(goal.target_pose.pose.position.y - self.start.pose.position.y) < 0.1):
            return True
        else:
            return False

    def killNodes(self):
        os.system("rosnode kill /boustrophedon_server")
        os.system("rosnode kill /boustrophedon_path_receiver_node")
        os.system("rosnode kill /polygon_client_node")
        os.system("rosnode kill /remote_bond")
        os.system("rosnode kill /robot_bond")
        os.system("rosnode kill /move_base")
        os.system("rosnode kill /amcl")
        os.system("rosnode kill /map_server")
        os.system("rosnode kill /robot_state_publisher")
        os.system("rosnode kill /turtlebot3_diagnostics")
        os.system("rosnode kill /turtlebot3_lds")
        os.system("rosnode kill /turtlebot3_core")

    def pathCallback(self, msg):
        print("I heard: x = ", msg.point.x, " y = ", msg.point.y)
        self.sendGoal(msg.point)

    def sendGoal(self, point):
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

        rospy.loginfo("Waiting for Server")
        client.wait_for_server()

        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = point.x
        goal.target_pose.pose.position.y = point.y
        goal.target_pose.pose.orientation.w = 1

        rospy.loginfo("Sending goal")
        client.send_goal(goal)

        wait = client.wait_for_result()

        if not wait:
            rospy.signal_shutdown("Action server not available!")
        else:
            return client.get_result()

        if(self.goalCounter > 5 and self.isGoalNearStart(goal)):
            self.killNodes()

        self.goalCounter += 1



if __name__ == '__main__':
    rospy.init_node('boustrophedon_path_receiver_node')
    path = PathHandler()
    rospy.spin()
