#!/usr/bin/env python3

import rospy, time
import roslaunch
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

#GMAPPING = 1
#HECTOR = 2
#SLAM_TOOLBOX = 3
#KARTO = 4

def setMissionIterations():
    mIterations = ""
    while(isinstance(mIterations, int)) is False:
        try:
            print("\x1b[0;33mEnter the number of missions you want to execute: \x1b[0;37m")
            mIterations = int(input())
        except:
            print("\x1b[1;31mInvalid input - Must be integer")

    return mIterations

def launchSlamMission(lFilePath):
    try:
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        parent = roslaunch.parent.ROSLaunchParent(uuid, [lFilePath])
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

#def slamInputCheck(input):
#    return(input==GMAPPING or input == HECTOR or input == SLAM_TOOLBOX or input == KARTO)

#def pollSLAMAlgorithm():
#    validInput = None
#    while(not slamInputCheck(validInput)):
#        try:
#            print("\n\x1b[0;33mPlease select the SLAM Algorithm (1 = gmapping, 2 = hector, 3 = slam_toolbox), 4 = karto: \x1b[0;37m")
#            validInput = int(input())
#            if(not slamInputCheck(validInput)):
#                print("\n\x1b[1;31mPlease select 1, 2, 3 or 4")
#        except:
#            print("\n\x1b[1;31mPlease select 1, 2, 3 or 4")
#
#    return validInput

if __name__=="__main__":
    test = 'true'

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('mission_control')

    mIterations = setMissionIterations()
    lFilePath = retrievePath()

    for x in range(mIterations):
        waitForUser(x+1)
        launchSlamMission(lFilePath)
        input()
        print("\n\x1b[1;92mMission {} complete".format(x+1))
