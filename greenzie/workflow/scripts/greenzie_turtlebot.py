#!/usr/bin/env python3

import os
import signal
from subprocess import *
import time
import argparse
import multiprocessing
import rospy
from std_msgs.msg import Int32


def writeFile(status, start_time):
    file = open("/home/joe/greenzie_catkin_ws/src/data/mission_status/runs_1_5", "a")
    if(status == 'failure'):
        file.write(start_time, " - ", time.strftime('%H%M%S'), ": failure\n")
    else:
        file.write(start_time, " - ", time.strftime('%H%M%S'), ": success\n")
    file.close()

def killNodes():
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

def get_stdout_stderr(typ, datetime, dir):
    out = '%s_%s_stdout.log' % (datetime, typ)
    err = '%s_%s_stderr.log' % (datetime, typ)
    return os.path.join(dir, out), os.path.join(dir, err)

def endProcess(process, name):
        print('Killing', name)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def startProcess(cmd, typ, start_time, logs):
    print('Starting', typ)

    stdout, stderr = get_stdout_stderr(typ, start_time, logs)
    with open(stdout, 'wb') as out, open(stderr, 'wb') as err:
        return run(cmd, stdout=out, stderr=err)

def checkExistance(files):
    for f in files:
        if not os.path.exists(f):
           raise ValueError('File does not exist: %s', f)

def missionLoop(args, mission_range):
    multiprocessing.set_start_method('spawn')
    
    for counter in range(mission_range):
        print("Press Enter to start the mission")
        input()
        print("Mission:", counter + 1)

        logs = args.logs
        coverage_server = args.server
        coverage_client = args.client
        path_receiver = args.path_receiver
        checkExistance([logs, coverage_server, coverage_client, path_receiver])

        # Record start time of server
        start_time = time.strftime('%H%M%S')

        server_node = multiprocessing.Process(target = startProcess, args = (['/bin/bash', coverage_server], 'server_node', start_time, logs))
        server_node.start()   

        path_receiver_node = multiprocessing.Process(target = startProcess, args = (['/bin/bash', path_receiver], 'server_node', start_time, logs))
        path_receiver_node.start()   

        time.sleep(2)
        
        print("Run remote.launch on the remote-pc to launch rosbag and dumpcap")

        time.sleep(2)  

        input("Press Enter to start client")

        client_start = time.strftime('%H%M%S')

        client_node = multiprocessing.Process(target = startProcess, args = (['/bin/bash', coverage_client], 'client_node', start_time, logs))
        client_node.start()

        time.sleep(2)

        fail_input = input("Press Enter to terminate the processes. Press 'f' to note mission failure, and terminate the processes.\n")
        if(fail_input == "f"):
            killNodes()
            writeFile('failure', client_start)
        else:
            writeFile('success', client_start)

        server_node.terminate()
        client_node.terminate()
        


if __name__ == '__main__':
    rospy.init_node('greenzie_workflow_node')

    mission_range = 1

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--logs', '-l', type=str, default='/home/joe/greenzie_catkin_ws/src/workflow/logs/turtlebot')
    parser.add_argument('--server', type=str, default='/home/joe/greenzie_catkin_ws/src/workflow/shell_scripts/boustrophedon_server.sh')
    parser.add_argument('--path_receiver', type=str, default='/home/joe/greenzie_catkin_ws/src/workflow/shell_scripts/path_receiver.sh')
    parser.add_argument('--client', type=str, default='/home/joe/greenzie_catkin_ws/src/workflow/shell_scripts/boustrophedon_client.sh')

    args = parser.parse_args()
    missionLoop(args, mission_range)
