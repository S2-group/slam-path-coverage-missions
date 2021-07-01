#!/usr/bin/env python3

import rospy, time
import roslaunch
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

GMAPPING = 1
HECTOR = 2
SLAM_TOOLBOX = 3
KARTO = 4

def setMissionIterations():
    mIterations = ""
    #checks if input is integer
    while(isinstance(mIterations, int)) is False:
        try:
            print("\x1b[0;33mEnter the number of missions you want to execute: \x1b[0;37m")
            mIterations = int(input())
        except:
            #throws error if not integer, loop repeats
            print("\x1b[1;31mInvalid input - Must be integer")

    return mIterations

def launchSlamSetup(lFilePath, slamMethod):
    try:
        #sets an argument to pass to launch file depending on algorithm chosen by user
        if(slamMethod == GMAPPING):
            arg1 = "slam_methods:=gmapping"
        if(slamMethod == HECTOR):
            arg1 = "slam_methods:=hector"
        if(slamMethod == SLAM_TOOLBOX):
            arg1 = "slam_toolbox:=true"
        if(slamMethod == KARTO):
            arg1 = "slam_methods:=karto"
        #generate UUID for launch file
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        #set arguments alongside launch file
        cliArgs = [lFilePath, arg1]
        roslaunchArgs = cliArgs[1:]
        #set launch file to run
        roslaunchFile= [(roslaunch.rlutil.resolve_launch_arguments(cliArgs)[0], roslaunchArgs)]
        parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunchFile)
        #start launch file
        parent.start()

    except:
        print("\n\x1b[1;31mError finding/running {}".format(lFilePath))
        exit()

def retrievePath():
    print("\n\x1b[0;33mPlease enter the full path of SLAM_robot.launch:\x1b[0;37m")
    lFilePath = input()
    return lFilePath

#verifies if SLAM algorithm chosen is one of the valid options
def slamInputCheck(input):
    return (input == GMAPPING or input == HECTOR or input == SLAM_TOOLBOX or input == KARTO)

def pollSLAMAlgorithm():
    validInput = None
    while(not slamInputCheck(validInput)):
        try:
            print("\n\x1b[0;33mPlease select the SLAM Algorithm (1 = gmapping, 2 = hector, 3 = slam_toolbox, 4 = karto): \x1b[0;37m")
            validInput = int(input())
            if(not slamInputCheck(validInput)):
                print("\n\x1b[1;31mPlease select 1, 2, 3 or 4")
        except:
            #tells user to input a valid value, loop repeats
            print("\n\x1b[1;31mPlease select 1, 2, 3 or 4")

    return validInput

def waitForUser(currentMission):
    print("\n\x1b[1;92mPress Enter key to begin mission {}".format(currentMission))
    input()

def killNodes(slamMethod):
    #list of commands used to kill nodes cleanly after mission execution
    os.system("rosnode kill /turtlebot3_lds")
    os.system("rosnode kill /turtlebot3_diagnostics")
    os.system("rosnode kill /turtlebot3_core")
    if(slamMethod == GMAPPING):
        os.system("rosnode kill /turtlebot3_slam_gmapping")
    if(slamMethod == HECTOR):
        os.system("rosnode kill /hector_mapping")
    if(slamMethod == SLAM_TOOLBOX):
        os.system("rosnode kill /slam_toolbox")
    if(slamMethod == KARTO):
        os.system("rosnode kill /slam_karto")

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    #initialize node
    rospy.init_node('SLAM_mission_control')

    #retrieves iterations from user
    mIterations = setMissionIterations()
    #retrieves path of SLAM_robot.launch from user
    lFilePath = retrievePath()

    #iterates through all missions
    for x in range(mIterations):
        #retrieves SLAM algorithm from user
        slamMethod = pollSLAMAlgorithm()
        #polls for enter input to stall until mission execution, x+1 = current mission number
        waitForUser(x+1)
        #launches mission
        launchSlamSetup(lFilePath, slamMethod)
        input()
        #kills nodes using system commands
        killNodes(slamMethod)
        print("\x1b[1;92mPlease wait...\x1b[0;37m")
        time.sleep(5)
        print("\n\x1b[1;92mMission {} complete".format(x+1))
