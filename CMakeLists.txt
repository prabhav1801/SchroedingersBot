cmake_minimum_required(VERSION 3.8)
project(schrodingers_bot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(vision_node vision_node.cpp)
ament_target_dependencies(vision_node rclcpp geometry_msgs OpenCV)

install(TARGETS
  vision_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
