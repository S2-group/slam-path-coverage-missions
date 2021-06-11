cmake_minimum_required(VERSION 2.8.3)
project(boustrophedon_client)

set(CMAKE_CXX_STANDARD 14)

find_package(catkin REQUIRED COMPONENTS
  rospy
  boustrophedon_msgs
  boustrophedon_server
  actionlib
  tf
  geometry_msgs
  nav_msgs
  rosparam_shortcuts
  genmsg
  std_msgs
)

find_package(CGAL REQUIRED COMPONENTS Core)

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS
  rospy
  boustrophedon_msgs
  actionlib
  tf
  geometry_msgs
  nav_msgs
  rosparam_shortcuts
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS scripts/boustrophedon_client_node.py scripts/boustrophedon_path_receiver_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


# include_directories(
#   include
#   ${catkin_INCLUDE_DIRS}
# )

# add_executable(boustrophedon_path_receiver_node src/boustrophedon_path_receiver_node.cpp)
# target_link_libraries(boustrophedon_path_receiver_node ${catkin_LIBRARIES})


# add_executable(boustrophedon_client_node src/boustrophedon_client_node.cpp)
# target_link_libraries(boustrophedon_client_node
#     ${catkin_LIBRARIES}
#     CGAL::CGAL
#     CGAL::CGAL_Core)

