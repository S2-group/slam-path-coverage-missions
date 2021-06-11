cmake_minimum_required(VERSION 3.0.2)
project(polygon_coverage_client)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  polygon_coverage_msgs
  rospy
  std_msgs
  actionlib
  move_base_msgs

)

catkin_package(
 LIBRARIES polygon_coverage_client
 CATKIN_DEPENDS geometry_msgs nav_msgs polygon_coverage_msgs rospy std_msgs
 DEPENDS system_lib
)

catkin_install_python(PROGRAMS scripts/polygon_client_node.py 
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
