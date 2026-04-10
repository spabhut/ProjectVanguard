cmake_minimum_required(VERSION 3.8)
project(rover)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(joint_state_publisher REQUIRED)       # NEW — needed for real HW
find_package(rviz2 REQUIRED)
find_package(xacro REQUIRED)
# REMOVED: gazebo_ros, gazebo_plugins

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(DIRECTORY
  launch
  urdf
  config
  rviz
  # REMOVED: worlds
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/teleop_key.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME teleop_key
)

ament_package()