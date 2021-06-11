#!/usr/bin/env python3

import psutil
from datetime import datetime
import time
import os
import rospy
from std_msgs.msg import String
import csv

def resource_writer():
    #retrieve time for filename
    now = str(time.time())
    #create filename
    path = '/home/ubuntu/ethz_catkin_ws/src/data/resource-meter/test-' + now + '.csv'
    #open csvfile
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        rospy.init_node('memory_writer', anonymous=True)
        cpu = 0
        #get csvfile ready to write
        csvwriter = csv.writer(csvfile)
        #loop until node is killed
        while not rospy.is_shutdown():
            cpu_old = cpu
            #get both formatted timestamps
            now1 = str(time.time())
            now2 = str(datetime.now())
            #get cpu usage
            cpu = str(psutil.cpu_percent())
            #it would sometimes throw a 0 value if polling too quickly
            #this is a way to remove these inaccuracies
            if(cpu == "0.0"):
                cpu = cpu_old
            #get memory usage
            mem = str(psutil.virtual_memory().percent)
            #write data to csv
            csvwriter.writerow([now1, now2, cpu, mem])
            time.sleep(0.01)

if __name__ == "__main__":
    resource_writer()
