# Greenzie Boustrophedon Planner

Configuration of [Greenzie's Boustrophedon Planner](https://github.com/Greenzie/boustrophedon_planner) package for usage with a Turtlebot. See the original repo for installation and licencing.

## TODO

* Turtlebot navigation parameters
* list of paths to change
* workflow package
  * This package includes the workflow script for running sequential missions. It also includes the remote and robot bond nodes which initiate the profilers.
* boustrophedon_client
  * client
  * path receiver node


## Mission Workflow

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




