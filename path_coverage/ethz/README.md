# ETHZ Polygon Coverage Planning

Configuration of [ETHZ ASL's Polygon Coverage Planning](https://github.com/ethz-asl/polygon_coverage_planning) package for usage with a Turtlebot. See the original repo for installation and licencing.

Follow the [Turtlebot documentation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) for turtlebot dependency installation and configuration.

## TODO

* Project Additions
* Move bond nodes to workflow
* Turtlebot navigation parameters
* list of paths to change


## Project Additions

* workflow package
  * This package includes the workflow script for running sequential missions. It also includes the remote and robot bond nodes which initiate the profilers.
* polygon_coverage_client
  * This package...
* Modification of polygon_coverage_ros coverage_planner.launch
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

Once ready, the workflow script will prompt you to launch the client, which subsequently launches the turtlebot bond node. This acquires the path from the polygon coverage server node and sends the points to the navigation stack.


The remote-pc bond node waits for the turtlebot bond node to be active, before starting rosbag record and dumpcap. The turtlebot bond node launches the resource-meter node. In this configuration, rosbag and the network and cpu profilers are recorded from the same timestamp.
