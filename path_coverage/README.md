# ROS Path Coverage


## General Setup

This project assumes the prior installation of ROS melodic or noetic.

These repositories are configured for the use with a ROBOTIS Turtlebot3 burger robot, see the [Turtlebot3 emanual](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) for setup and configuration instructions.

A good start point for running these path coverage packages is to run a basic navigate-to-goal mission. Follow these tutorials on [SLAM](https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/) and [navigation](https://emanual.robotis.com/docs/en/platform/turtlebot3/navigation/) for guidance. It may also be helpful to run these missions in a Gazebo simulated environment first. See this [tuturial](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/) for setup instructions.

To run these path coverage packages on a physical Turtlebot3, see this [README](https://github.com/S2-group/ros-configurations/tree/main/raspberrypi) for an Ubuntu image for the Raspberry Pi as well as detailed setup instructions.

## Connecting to the Turtlebot3

Having turned the Turtlebot3 on, SSH into it with the following command:

```
$ ssh ubuntu@<ip-of-turtlebot3>
```

To save having to enter the specific IP of the Turtlebot3 into various commands (including the above one), it is possible to set names to the various IPs active in the system. This can be done using:

```
$ sudo nano /etc/hosts
```

You can then give the IPs associated names, for example:

![ips](https://user-images.githubusercontent.com/22135172/124393018-b9139300-dcf8-11eb-8576-4efb9c994120.png)


This can be done on both the Turtlebot3 itself and the remote PC. Connecting to the Turtlebot3 can then be done via a command such as:

```
$ ssh ubuntu@turtlebot
```

It is important to ensure the connection between the Turtlebot3 and the remote PC is sound, otherwise running the required ```turtlebot3_bringup``` package will fail and the robot will not be responsive. This is covered in the [Turtlebot3 setup documentation](), your .bashrc files should look something like this:

Remote PC:

![remote_pc_bash](https://user-images.githubusercontent.com/22135172/124393392-93878900-dcfa-11eb-8662-d537d6d476b5.png)

Turtlebot3:

![tb_bash](https://user-images.githubusercontent.com/22135172/124393494-1a3c6600-dcfb-11eb-80d0-25e3725774bb.png)




## Time synchronisation

To resolve any time synchronisation issues between the Turtlebot3 and the remote PC, install chrony on both machines:

```
$ sudo apt-get install chrony
```

See this [ROS wiki post](https://answers.ros.org/question/298821/tf-timeout-with-multiple-machines/?fbclid=IwAR3k63RvLPDzuJAN2bOpsutWqLcIfxDx0074DkxehJZgAbNC29TbOw9afHE) for more detailed instructions and proper setup.

## Navigation Parameters

In order to premote straight line traversals, various navigation parameters were tweaked. See navigation_params for the differing parameter/launch files from the turtlebot3_navigation package. They can be summaried in this table:

| Parameter  | Default | Optimal |
| ------------- | ------------- | ------------- |
| path_distance_bias  | 32.0  | 5.0  |
| goal_distance_bias  | 20.0  | 30.0  |
| sim_time  | 1.5  | 2.5  |
| max_vel_x  | 0.22  | 0.18  |
| min_vel_x  | -0.22  | -0.18  |
| forward_point_distance  | 0.325  | 0.0  |
| xy_goal_tolerance  | 0.05  | 0.15  |
| yaw_goal_tolerance  | 0.17  | 3.14  |
| stripe_seperation (Greenzie specific)  | 1.0  | 0.5  |

## Profiler Setup

The profilers require the following dependencies to be installed to function:

- bondpy
- pyrosbag
- psutil

They can be installed using pip:

```
$ pip3 install <dependency>
```


## Map and Polygon Coordinates

Before running these path coverage packages, some information about the Turtlebot3's environment must be known in advance. The first of which is the map itself. A map can be acquired using the Turtlebot3's SLAM packages, information of how to use such packages can be found [here](https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/). It is worth noting that the [Greenzie planner]() does not work with concave arenas or arenas that have internal obstacles.

The coordinates of the mission arena are also required as input to the planners. To this end, a set_arena ROS node was implemented which records the current position of the robot at each corner of the arena boundary. 

Having set up a basic navigation using teleop_keyboard operation, run the following:

```
$ roslaunch set_arena set_arena_node.launch 
```

Then navigate the Turtlebot3 to the first corner point in the arena. You will be prompted to press 'p' on the keypad, pressing this will record the current coordinates of the robot. Repeat this for all corner points in the arena. Pressing 's' on the keypad will publish the coordinates to text files: x_coordinates.txt and y_coordinates.txt. The path of these files will used in the planner setup step, see the specific planner READMEs for more information.



 
