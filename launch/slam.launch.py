from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    parameters = [{
        'frame_id': 'base_link',
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'approx_sync': True,
        'wait_for_transform': 0.5,         # slightly longer for real TF
        'Grid/RangeMax': '5.0',
        'use_sim_time': False              # CHANGED
    }]

    # Topic names now match the realsense2_camera_node's namespace='d455'
    remappings = [
        ('rgb/image',        '/d455/color/image_raw'),      # CHANGED
        ('rgb/camera_info',  '/d455/color/camera_info'),    # CHANGED
        ('depth/image',      '/d455/depth/image_rect_raw'), # CHANGED
        ('odom',             '/odom'),
        ('grid_map',         '/map')
    ]

    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=parameters,
        remappings=remappings,
        arguments=['-d']
    )

    return LaunchDescription([rtabmap_node])