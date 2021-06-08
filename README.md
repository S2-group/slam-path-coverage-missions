## Setup
This setup assumes you already have ROS installed (melodic or noetic) on your computer.

In order to run the missions with the physical burger bot (turtlebot3), you will need to follow the following tutorials for setting up the robot:

- The tutorial to install the ubuntu image on the Raspberry Pi found in S2-group/ros-configurations/raspberrypi on Github
- This tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/ (make sure to select the correct ROS version).
Note: It is highly recommended to add the export ROS_MASTER_URI and export ROS_HOSTNAME lines to the .bashrc file as indicated in the tutorial. The same applies on the Raspberry Pi
- This tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/ to allow the Raspberry Pi to communicate with the OpenCR board
- The tutorial to set up the power reading arduino in S2-group/ros-configurations/meter-arduino

You can test if all these were installed properly by sourcing ROS (source /opt/ros/[version]/setup.bash), running roscore, running bringup on the robot, and then running the teleoperation node from your computer as per this tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/basic_operation/

You will also need to install the following ROS packages on your remote PC:
- turtlebot3_simulations (if you want to simulate it in gazebo)

And the following ROS packages on your Turtlebot:
- ```$ sudo apt-get install ros-[version]-gmapping```
- ```$ sudo apt-get install ros-[version]-hector-slam```
- ```$ sudo apt-get install ros-[version]-slam-karto```
- ```$ sudo apt-get install ros-[version]-slam-toolbox```
- turtlebot3_slam

In order for the python files to run correctly, you'll need to install:
- ```pip3 install bondpy```
- ```pip3 install pyrosbag``` (remote PC only)
- ```pip3 install psutil``` (turtlebot only)

Now the folders for the data collection should be created.

Remote PC:
- A folder for your rosbag files (can be anywhere)
- A folder for your network data - simply create the folder "Robot_Data" in your /home/[username]/ directory.

Turtlebot:
- A folder for your cpu/mem profiler data named Robot_Data (should have the path /home/ubuntu/Robot_Data)

For the remote PC, here are the environment variables you should be setting in .bashrc (```sudo nano .bashrc```):
- export ROS_MASTER_URI=http://[remote-pc-ip]:11311/
- export ROS_HOSTNAME=[remote-pc-ip]
- export TURTLEBOT3_MODEL=burger
- export PATH_TO_BAG=/path/to/where/bagfile/should/be/stored/SLAM.bag

![alt text](https://i.imgur.com/rAjnJcO.png)

For the turtlebot, here are the environment variables you should set in .bashrc:
- export ROS_MASTER_URI=http://[remote-pc-ip]:11311/
- export ROS_HOSTNAME=[turtlebot-ip]
- export TURTLEBOT3_MODEL=burger
- sudo ntpdate -q [remote-pc-ip]

![alt text](https://i.imgur.com/7P3y6IS.png)

Anything ip indicated by [name] should be replaced by the actual ip of the turtlebot/remote pc. In order to retrieve the IP of both machines, use `ifconfig`

In order for the network profiler to work on the remote PC, you will also have to:
`sudo nano /etc/hosts`
and add the turtlebot ip to the list of known IP's with the name "turtlebot-ip" like this: <br/>
![alt text](https://i.imgur.com/3igYluE.png)

And finally, if you face time synchronization issues, you'll need to install chrony on the PC and the turtlebot:
```bash
$ sudo apt-get install chrony
```
and follow this tutorial: https://answers.ros.org/question/298821/tf-timeout-with-multiple-machines/?fbclid=IwAR3k63RvLPDzuJAN2bOpsutWqLcIfxDx0074DkxehJZgAbNC29TbOw9afHE

## Running
-run Setup
-run main mission
-collect data
-arduino?
