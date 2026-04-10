from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    remappings = [
        ('rgb/image',       '/d455/d455/color/image_raw'),
        ('rgb/camera_info', '/d455/d455/color/camera_info'),
        ('depth/image',     '/d455/d455/depth/image_rect_raw'),
        ('imu',             '/d455/d455/imu')
    ]

    visual_odometry_node = Node(
        package='rtabmap_odom',
        executable='rgbd_odometry',
        name='visual_odometry',
        output='screen',
        parameters=[{
            'frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'publish_tf': True,
            'approx_sync': True,
            'use_sim_time': False,
            'wait_imu_to_init': True
        }],
        remappings=remappings
    )

    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',  # Headless backend node, keeps GUI in RViz
        name='rtabmap',
        output='screen',
        parameters=[{
            'frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'subscribe_depth': True,
            'subscribe_rgb': True,
            'subscribe_odom': True,
            'publish_tf': True,
            'approx_sync': True,
            'use_sim_time': False,
            'Grid/RangeMax': '5.0',
            'Mem/IncrementalMemory': 'true'
        }],
        remappings=remappings + [('grid_map', '/map')],
        arguments=['-d']
    )

    return LaunchDescription([
        visual_odometry_node,
        rtabmap_node
    ])