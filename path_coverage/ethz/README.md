# ETHZ Polygon Coverage Planning

Configuration of [ETHZ ASL's Polygon Coverage Planning](https://github.com/ethz-asl/polygon_coverage_planning) package for usage with a Turtlebot. See the original repo for installation and licencing.

Follow the [Turtlebot documentation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) for turtlebot dependency installation and configuration.

## TODO

* Move bond nodes to workflow
* Turtlebot navigation parameters
* list of paths to change
* workflow package
  * This package includes the workflow script for running sequential missions. It also includes the remote and robot bond nodes which initiate the profilers.
* polygon_coverage_client
  * This package...
* Modification of polygon_coverage_ros coverage_planner.launch
  * ...

## Installation Pointers

* ...

## Mission Workflow

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
