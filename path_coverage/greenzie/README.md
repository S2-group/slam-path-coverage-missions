# Greenzie Boustrophedon Planner

Configuration of [Greenzie's Boustrophedon Planner](https://github.com/Greenzie/boustrophedon_planner) package for usage with a Turtlebot. See the original repo for installation and licencing.

## TODO

* boustrophedon_client
  * client
  * path receiver node


## Mission Workflow

The workflow ROS package was made to provide a consistent mission execution process for both path coverage algorithms. The package includes a workflow script for running sequential missions, along with remote and robot bond nodes which initiate the data profilers (psutil, dumpcap etc.).

Ensure the repository is built on both the remote-pc and the turtlebot, see link above.

First run roscore on the remote-pc:

```
$ roscore
```

Run the mission workflow script on the turtlebot:

```
$ rosrun workflow greenzie_turtlebot.py
```

Running this on the turtlebot launches the following:
- Turtlebot3 bringup
- Turtlebot3 navigation
- boustrophedon_server

You will be prompted to launch the remote-pc launch file, which launches the remote-pc bond node:

```
$ roslaunch workflow remote.launch
```

``` remote.launch ``` starts ``` remote_bond.py ```, which waits for ``` robot_bond.py ``` to be launched, before starting the recording of rosbag and dumpcap.


The workflow script will prompt you to launch the client, which subsequently launches ``` robot_bond.py ```. The client sends the polygon coordinates to the server. The goal coordinates are then retreived by the ``` boustrophedon_path_receiver_node.py ``` and parsed to the navigation stack. ``` robot_bond.py ``` launches the resource-meter node. 

The bond functionality allows the rosbag and network/cpu profilers to be recorded from the same timestamp.


## Workflow Timeline

![workflow](https://user-images.githubusercontent.com/22135172/126071268-4b75f676-e686-4ac9-abd7-10e3ced08e96.png)

## Workflow Screenshot

![greenzie_workflow](https://user-images.githubusercontent.com/22135172/126071322-c59cea1e-efa1-4602-8f1f-d84b8daf7d83.png)

## Paths to change

* boustrophedon_client/scripts/boustrophedon_client_node.py
  * Path to x & y coordinates in parseValues method
* workflow/launch/profilers.launch
  * Path to desired directory of collected rosbags
* workflow/scripts/dumpcap.sh
  * Path to desired directory of collected dumpcap data
* workflow/scripts/greenzie_turtlebot.py
  * Path to mission_status file (records success/failure of mission)
  * Paths to client and server shell scripts
* workflow/scripts/remote_bond.py
  * Path to profilers.launch
* workflow/scripts/resource_meter.py
  * Path to desired directory of psutil data
* workflow/scripts/robot_bond.py
  * Path to resource_meter.launch


