import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('rover')
    explore_params = os.path.join(pkg_dir, 'config', 'explore.yaml')

    explore_node = Node(
        package='explore_lite',
        executable='explore',
        name='explore',
        output='screen',
        parameters=[
            explore_params,
            {'use_sim_time': True}
        ]
    )

    return LaunchDescription([explore_node])
