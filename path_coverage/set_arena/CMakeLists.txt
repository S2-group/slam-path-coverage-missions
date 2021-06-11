cmake_minimum_required(VERSION 3.0.2)
project(set_arena)

set(CMAKE_CXX_STANDARD 14)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  std_msgs
)


catkin_package(
 INCLUDE_DIRS include
 LIBRARIES set_arena
 CATKIN_DEPENDS geometry_msgs roscpp std_msgs
 DEPENDS system_lib
)


include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(set_arena_node src/set_arena_node.cpp)
target_link_libraries(set_arena_node ${catkin_LIBRARIES})
