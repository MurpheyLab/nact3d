cmake_minimum_required(VERSION 2.8.3)
project(nact3d)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs geometry_msgs visualization_msgs genmsg message_generation)

add_message_files(FILES cursor.msg)
add_message_files(FILES cursor_dyn.msg)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(
   # INCLUDE_DIRS include
   CATKIN_DEPENDS rospy roscpp std_msgs geometry_msgs genmsg visualization_msgs message_runtime
)

include_directories(include
  ${catkin_INCLUDE_DIRS}
)
