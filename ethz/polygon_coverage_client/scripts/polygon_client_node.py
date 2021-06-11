#!/usr/bin/env python
import rospy
import os
import actionlib
from geometry_msgs.msg import Point32
from polygon_coverage_msgs.srv import PolygonService
from polygon_coverage_msgs.msg import PolygonWithHolesStamped
from geometry_msgs.msg import Point32
from polygon_coverage_msgs.srv import PlannerService
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def killNodes():
    os.system("rosnode kill /coverage_planner")
    os.system("rosnode kill /polygon_client_node")
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

def sendGoal(point):
    #print("x", point.transforms[0].translation.x)
    #print("y", point.transforms[0].translation.y)

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for Server")
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = point.transforms[0].translation.x
    goal.target_pose.pose.position.y = point.transforms[0].translation.y
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1

    rospy.loginfo("Sending goal")
    client.send_goal(goal)

    wait = client.wait_for_result()
    
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def retrievePath():
    rospy.loginfo("Waiting for /plan_path service")
    rospy.wait_for_service('/coverage_planner/plan_path')
    try:
        set_poses = rospy.ServiceProxy('/coverage_planner/plan_path', PlannerService)
        
        start_end_pose = PoseStamped()
        
        start_end_pose.header.stamp = rospy.Time.now()
        start_end_pose.header.frame_id = "map"
        start_end_pose.pose.position.x = -0.19
        start_end_pose.pose.position.y = 0.64
        start_end_pose.pose.position.z = 0.0
        
        start_pose = start_end_pose 
        goal_pose = start_end_pose

        response = set_poses(start_pose, goal_pose)
        rospy.loginfo(response.success)

    except rospy.ServiceException as e:
        rospy.logerr("Service call failed")

    return response

def parseValues(axis):  
    points = []
    
    try:
        with open("/home/ubuntu/ethz_catkin_ws/src/maps/arena/" + axis + "_coordinates.txt") as file_reader:
            line = file_reader.readline()
            while line != '':
                points.append(float(line.rstrip("\n")))
                line = file_reader.readline()
    except:
        rospy.logerr("Could not process the file - " + axis + "_coordinates.txt")

    return points



if __name__ == '__main__':
    rospy.init_node('polygon_client_node')

    x_points = parseValues("x")
    y_points = parseValues("y")

    points32 = []

    if(len(x_points) != len(y_points)):
        raise Exception("Incomplete Coordinates")

    for i in range(len(x_points)):
        if(i == 0):
            points32.append(Point32(x_points[i], y_points[i], 1.0))
        else:
            points32.append(Point32(x_points[i], y_points[i], 0.0))

    rospy.wait_for_service('/coverage_planner/set_polygon')
    try:
        set_poly_srv = rospy.ServiceProxy('/coverage_planner/set_polygon', PolygonService)

        polygon_msgs = PolygonWithHolesStamped()
        polygon_msgs.header.stamp = rospy.Time.now()
        polygon_msgs.header.frame_id = "map"
        polygon_msgs.polygon.hull.points = points32

        response = set_poly_srv(polygon_msgs)

        if(response.success):
            response = retrievePath()
            if(response.success):
                for point in response.sampled_plan.points:
                    sendGoal(point)


        killNodes()

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e) 
