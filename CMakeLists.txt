cmake_minimum_required(VERSION 2.8.3)
project(t265_json)

#find_package(catkin REQUIRED )
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs message_generation)



add_message_files(
  FILES
  JSON.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package()
