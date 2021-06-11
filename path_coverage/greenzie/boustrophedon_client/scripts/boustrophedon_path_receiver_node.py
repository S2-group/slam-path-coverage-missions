#!/usr/bin/env python

import rospy
import os
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PointStamped

class PathHandler:
    goalCounter = 0
    start_finish_goal = PointStamped()
    
    def __init__(self):
        rospy.loginfo("Waiting for path points")
        rospy.Subscriber("/boustrophedon_server/path_points", PointStamped, self.pathCallback)

    def killNodes(self):
        os.system("rosnode kill /boustrophedon_server")
        os.system("rosnode kill /remote_bond")
        os.system("rosnode kill /robot_bond")
        os.system("rosnode kill /resource_meter")
        os.system("rosnode kill /move_base")
        os.system("rosnode kill /amcl")
        os.system("rosnode kill /map_server")
        os.system("rosnode kill /robot_state_publisher")
        os.system("rosnode kill /turtlebot3_diagnostics")
        os.system("rosnode kill /turtlebot3_lds")
        os.system("rosnode kill /turtlebot3_core")
        os.system("rosnode kill /boustrophedon_path_receiver_node")

    def pathCallback(self, msg):
        print("I heard: x = ", msg.point.x, " y = ", msg.point.y)
        self.sendGoal(msg.point)

    def sendGoal(self, point):
        if(self.goalCounter == 0):
            self.start_finish_goal = point
        
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
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            if(self.goalCounter > 0 and point == self.start_finish_goal):
                self.killNodes()
        self.goalCounter += 1    
        return client.get_result()       



if __name__ == '__main__':
    rospy.init_node('boustrophedon_path_receiver_node')
    path = PathHandler()
    rospy.spin()
