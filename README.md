## Setup
This setup assumes you already have ROS installed (melodic or noetic) on your computer.

In order to run the missions with the physical burger bot (turtlebot3), you will need to follow the following tutorials for setting up the robot:

- The tutorial to install the ubuntu image on the raspberry pi found in S2-group/ros-configurations/raspberrypi on Github
- This tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/ (make sure to select the correct ROS version).
Note: It is highly recommended to add the export ROS_MASTER_URI and export ROS_HOSTNAME lines to the .bashrc file as indicated in the tutorial. The same applies on the Raspberry Pi
- This tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/ to allow the Raspberry Pi to communicate with the OpenCR board

You can test if all these were installed properly by sourcing ROS (source /opt/ros/[version]/setup.bash), running roscore, running bringup on the robot, and then running the teleoperation node from your computer as per this tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/basic_operation/

You will also need to install the following ROS packages on your remote PC:
- turtlebot3_simulations (if you want to simulate it in gazebo)

And the following ROS packages on your Turtlebot:
- ```bash
$ sudo apt-get install ros-[version]-gmapping
```
- hector
- karto
- slam_toolbox
- turtlebot3_slam

In order for the python files to run correctly, you'll need to install:
- bondpy
- roslaunch
- pyrosbag (remote PC only)
- psutil (turtlebot only)

And finally, if you face time synchronization issues, you'll need to install chrony on the PC and the turtlebot:
```bash
$ sudo apt-get install chrony
```
and follow this tutorial: https://answers.ros.org/question/298821/tf-timeout-with-multiple-machines/?fbclid=IwAR3k63RvLPDzuJAN2bOpsutWqLcIfxDx0074DkxehJZgAbNC29TbOw9afHE

## Running
