from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():

    parameters = [{
        # --- Core Setup ---
        'frame_id': 'base_footprint',
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'approx_sync': True,
        'wait_for_transform': 1.0,
        'use_sim_time': True,
        'qos_image': 2,
        'qos_camera_info': 2,
        'qos_imu': 2,
    }]

    remappings = [
        ('rgb/image',        '/limo/depth_camera_link/image_raw'),
        ('rgb/camera_info',  '/limo/depth_camera_link/camera_info'),
        ('depth/image',      '/limo/depth_camera_link/depth/image_raw'),
        ('odom',             '/odom'),
        ('grid_map',         '/map'),
    ]

    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=parameters,
        remappings=remappings,
        arguments=['-d'] # -d deletes the old database so you get a fresh map every run
    )


    return LaunchDescription([rtabmap_node])