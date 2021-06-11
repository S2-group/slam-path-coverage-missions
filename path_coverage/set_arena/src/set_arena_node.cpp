#include <iostream>
#include <stdio.h>
#include <vector>
#include "ros/ros.h"
#include "geometry_msgs/PoseWithCovarianceStamped.h"
#include "geometry_msgs/Point.h"
#include <std_msgs/Float64.h>
#include <sstream>
#include <fstream>
#include <iterator>


geometry_msgs::Point getAmclPoint(){
    boost::shared_ptr<geometry_msgs::PoseWithCovarianceStamped const> shared_pose;
    geometry_msgs::PoseWithCovarianceStamped cur_pose;

    shared_pose = ros::topic::waitForMessage<geometry_msgs::PoseWithCovarianceStamped>("/amcl_pose", ros::Duration(10));
    if (shared_pose == NULL){
        ROS_INFO("No amcl pose messages received");
    }          
    else{
        cur_pose = *shared_pose;
    }     
    return cur_pose.pose.pose.position;
}

int main(int argc, char **argv){
    ros::init(argc, argv, "set_arena_node");

    std::vector<double> x_points;
    std::vector<double> y_points;

    ROS_INFO("Enter the polygon coordinates");
    ROS_INFO("'p' = Mark Coordinate, 's' = Submit Coordinates");

    char input;
    bool live = true;

    while(live){
        std::cin >> input;
        if(input == 'p'){
            std::cout << "Coordinate Marked\n";
            x_points.push_back(getAmclPoint().x);
            y_points.push_back(getAmclPoint().y);
        }
        else if(input == 's'){
            std::cout << "Polygon Submitted\n";
            live = false;
        }
    }

    std::ofstream outFile_x("/home/joe/catkin_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models/arena/x_coordinates.txt");
    for (const auto &e : x_points) outFile_x << e << "\n";

    std::ofstream outFile_y("/home/joe/catkin_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models/arena/y_coordinates.txt");
    for (const auto &e : y_points) outFile_y << e << "\n";
    
    return 0;
}
 
