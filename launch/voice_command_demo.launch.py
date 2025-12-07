from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        # Voice command processing node
        Node(
            package='voice_processing',
            executable='voice_command_node',
            name='voice_command',
            output='screen',
            parameters=[
                {'model_name': 'base'},
                {'sample_rate': 16000}
            ]
        ),

        # Object detection node
        Node(
            package='object_detection',
            executable='object_detector_node',
            name='object_detector',
            output='screen',
            parameters=[
                {'confidence_threshold': 0.7},
                {'model_name': 'grounding_dino'}
            ]
        ),

        # Robot controller node
        Node(
            package='robot_control',
            executable='robot_controller_node',
            name='robot_controller',
            output='screen',
            parameters=[
                {'planning_time': 5.0},
                {'execution_timeout': 30.0}
            ]
        ),

        # TF broadcaster for coordinate transforms
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_pub',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'camera_link']
        )
    ])