cmake_minimum_required(VERSION 3.0.2)
project(workflow)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES workflow
#  CATKIN_DEPENDS rospy
#  DEPENDS system_lib
)

catkin_install_python(PROGRAMS scripts/greenzie_turtlebot.py scripts/remote_bond.py scripts/resource_meter.py scripts/robot_bond.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
