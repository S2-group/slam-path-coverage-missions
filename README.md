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
- ```$ pip3 install bondpy```
- ```$ pip3 install pyrosbag``` (remote PC only)
- ```$ pip3 install psutil``` (turtlebot only)
- ```$ pip3 install defusedxml``` (turtlebot only)

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

Any ip indicated by [name] should be replaced by the actual ip of the turtlebot/remote pc. In order to retrieve the IP of both machines, use `ifconfig`

In order for the network profiler to work on the remote PC, you will also have to:
`sudo nano /etc/hosts`
and add the turtlebot ip to the list of known IP's with the name "turtlebot-ip" like this: <br/>
![alt text](https://i.imgur.com/3igYluE.png)

And finally, if you face time synchronization issues, you'll need to install chrony on the PC and the turtlebot:
```bash
$ sudo apt-get install chrony
```
and follow this tutorial: https://answers.ros.org/question/298821/tf-timeout-with-multiple-machines/?fbclid=IwAR3k63RvLPDzuJAN2bOpsutWqLcIfxDx0074DkxehJZgAbNC29TbOw9afHE

In order to run the missions, you will also have to create a catkin workspace. To do this, simply open a directory of your choice and run: <br/>
```bash
 $ mkdir -p catkin_ws/src
 ```

After this, place the s2_slam package into the src folder. Once you've done this, run: <br/>
```bash
$ cd /.../catkin_ws
$ source /opt/ros/noetic/setup.bash
$ catkin_make
```

A build and devel folder should be generated within the catkin_ws folder.
Do this on both the remote PC and the turtlebot.

## Running

First you need to source ROS on the remote PC to run roscore: <br/>
```bash
$ source /opt/ros/noetic/setup.bash
$ roscore
```

Now turn on the turtlebot and open a terminal to ssh into it:
```bash
$ ssh ubuntu@turtlebot-ip
```

Once connected, source the workspace on the remote PC:
```bash
$ source /path/to/catkin_ws/devel/setup.bash
```

Source the ROS environment on the turtlebot to run turtlebot3_robot.launch:
```bash
$ source /opt/ros/noetic/setup.bash
$ roslaunch turtlebot3_bringup turtlebot3_robot.launch
```

Now you can run the setup launch file on the remote PC:
```bash
$ roslaunch s2_slam SLAM_mission_setup.launch
```

With this running, you can teleoperate the robot to record the path it will take. Once the map on RVIZ is complete, you can kill the running nodes on the remote PC to stop recording to the bag file.

Next you should source the catkin_ws workspace on the turtlebot:
```bash
$ source /path/to/catkin_ws/devel/setup.bash
```

Now you can run the mission controller on the remote PC:
```bash
$ rosrun s2_slam remote_SLAM_controller.py
```
and on the robot:
```bash
$ rosrun s2_slam robot_SLAM_controller.py
```

Once both running, fill in all fields polled by the programs. Once you've done this, both terminals should say "Press enter key to begin mission 1" <br/>
![alt text](https://i.imgur.com/1cmvOLS.png)

Now you can start the arduino power meter by pressing the button. (WARNING: make sure to plug the arduino into the turtlebot after turning it on, as it can get confused about the arduino and try to use the port it is connected to in order to communicate with the OpenCR board)

Then press enter on the turtlebot controller first, wait until the terminal says "Calibration end". After that you can press enter on the remote PC.  <br/>
![alt text](https://i.imgur.com/YKBv5MN.png)

For all mission executions, remember to allow the robot_SLAM_controller to reach "Calibration end" before starting the remote_SLAM_controller mission execution.

In order to retrieve data files off the robot after all missions have executed, run:
```bash
$ sudo is_shutdown
```
on the turtlebot. Once it is fully shutdown (ssh disconnects), it is safe to power off the robot with the switch and remove the SD to retrieve the files manually on the remote PC. 
