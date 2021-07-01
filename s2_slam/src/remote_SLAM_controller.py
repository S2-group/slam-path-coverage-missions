#!/usr/bin/env python3

import rospy, time
import roslaunch
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

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

def launchSlamMission(lFilePath):
    try:
        #generate UUID for launch file
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        #set launch file to run
        parent = roslaunch.parent.ROSLaunchParent(uuid, [lFilePath])
        #start launch file
        parent.start()

    except:
        print("\n\x1b[1;31mError finding/running {}".format(lFilePath))
        exit()

def retrievePath():
    print("\n\x1b[0;33mPlease enter the full path of SLAM_mission.launch: \x1b[0;37m")
    lFilePath = input()
    return lFilePath

def waitForUser(currentMission):
    print("\n\x1b[1;92mPress Enter key to begin mission {}".format(currentMission))
    input()

if __name__=="__main__":
    test = 'true'

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
    #initializes node
    rospy.init_node('mission_control')

    #retrieves iterations from user
    mIterations = setMissionIterations()
    #retrieves SLAM_mission.launch file path from user
    lFilePath = retrievePath()

    #iterates through all the missions
    for x in range(mIterations):
        #polls for enter input to stall until mission execution, x+1 = current mission number
        waitForUser(x+1)
        #launches mission
        launchSlamMission(lFilePath)
        #wait until use presses enter to stop mission
        input()
        print("\n\x1b[1;92mMission {} complete".format(x+1))
