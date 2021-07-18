# ETHZ Polygon Coverage Planning

Configuration of [ETHZ ASL's Polygon Coverage Planning](https://github.com/ethz-asl/polygon_coverage_planning) package for usage with a Turtlebot. See the original repo for installation and licencing.

## TODO

* polygon_coverage_client
  * This package...
* Modification of polygon_coverage_ros coverage_planner.launch
  * ...

## Mission Workflow

The workflow ROS package was made to provide a consistent mission execution process for both path coverage algorithms. The package includes a workflow script for running sequential missions, along with remote and robot bond nodes which initiate the data profilers (psutil, dumpcap etc.).

Ensure the repository is built on both the remote-pc and the turtlebot, see link above.

First run roscore on the remote-pc:

```
$ roscore
```

Run the mission workflow script on the turtlebot:

```
$ rosrun workflow ethz_turtlebot.py
```

Running this on the turtlebot launches the following:
- Turtlebot3 bringup
- Turtlebot3 navigation (ommiting rviz)
- Polygon coverage server

You will then be prompted to launch the remote-pc launch file, which launches rviz and the remote-pc bond node:

```
$ roslaunch workflow remote.launch
```

``` remote.launch ``` starts ``` remote_bond.py ```, which waits for ``` robot_bond.py ``` to be launched, before starting the recording of rosbag and dumpcap.


The workflow script will prompt you to launch the client, which subsequently launches ``` robot_bond.py ```. The client sends the polygon coordinates to the server and retreives the goal coordinates, which are then parsed to the navigation stack. ``` robot_bond.py ``` launches the resource-meter node. 

The bond functionality allows the rosbag and network/cpu profilers to be recorded from the same timestamp.

## Paths to change

* polygon_coverage_client/scripts/polygon_client_node.py
  * Path to x & y coordinates in parseValues method
* workflow/launch/profilers.launch
  * Path to desired directory of collected rosbags
* workflow/scripts/dumpcap.sh
  * Path to desired directory of collected dumpcap data
* workflow/scripts/ethz_turtlebot.py
  * Path to mission_status file (records success/failure of mission)
  * Paths to client and server shell scripts
* workflow/scripts/remote_bond.py
  * Path to profilers.launch
* workflow/scripts/resource_meter.py
  * Path to desired directory of psutil data
* workflow/scripts/robot_bond.py
  * Path to resource_meter.launch

## Workflow Timeline

![workflow](https://user-images.githubusercontent.com/22135172/126071268-4b75f676-e686-4ac9-abd7-10e3ced08e96.png)

## Workflow Screenshot

![ethz_workflow](https://user-images.githubusercontent.com/22135172/126071299-95f3c2f5-f32b-4e45-8265-2df9b5137a8c.png)

