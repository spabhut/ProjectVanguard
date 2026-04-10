import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'rover'
    pkg_dir = get_package_share_directory(pkg_name)

    xacro_file = os.path.join(pkg_dir, 'urdf', 'rover.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'rover.rviz')

    # Robot State Publisher — use_sim_time is now FALSE
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': False          # CHANGED
        }]
    )

    # Joint State Publisher — publishes wheel joint states on real HW
    # Replace with your actual motor driver node once available
    jsp_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': False}]
    )

    # Intel RealSense D455
    realsense_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='d455',
        namespace='d455',
        output='screen',
        parameters=[{
            'serial_no': '',               # leave blank to auto-detect
            'enable_depth': True,
            'enable_color': True,
            'depth_width': 640,
            'depth_height': 480,
            'depth_fps': 30,
            'color_width': 640,
            'color_height': 480,
            'color_fps': 30,
            'align_depth.enable': True,
            'pointcloud.enable': True,
            'enable_gyro': True,           # D455 has IMU
            'enable_accel': True,
            'unite_imu_method': 'linear_interpolation',
            'use_sim_time': False
        }]
    )

    # RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': False}]    # CHANGED
    )

    return LaunchDescription([
        rsp_node,
        jsp_node,          # NEW
        realsense_node,    # NEW
        rviz_node,
        # REMOVED: gazebo, spawn_node
    ])