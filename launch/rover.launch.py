import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. Package Directories
    pkg_rover = get_package_share_directory('rover')
    pkg_limo_desc = get_package_share_directory('limo_description')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # 2. File Paths
    urdf_file_path = os.path.join(pkg_limo_desc, 'urdf', 'limo_four_diff.xacro')
    rviz_config_file = os.path.join(pkg_rover, 'rviz', 'rover.rviz')
    world_path = os.path.join(pkg_rover, 'worlds', 'rover.world') # Clean path to rover.world

    # 3. Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # 4. Nodes & Includes
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world_path}.items()
    )

    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    )

    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_file_path]),
            'use_sim_time': use_sim_time
        }]
    )

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    spawn_entity_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'limo', 
            '-topic', 'robot_description', 
            '-x', '0.0', '-y', '0.0', '-z', '0.0', '-Y', '0.0'
        ],
        output='screen'
    )

    # Sequence ensuring spawn happens securely alongside RViz
    spawn_after_rviz = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=start_rviz_cmd,
            on_start=[spawn_entity_cmd]
        )
    )

    # 5. Build the Launch Description
    ld = LaunchDescription()
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='true', description='Use sim time'))
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_joint_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)
    ld.add_action(spawn_after_rviz)

    return ld