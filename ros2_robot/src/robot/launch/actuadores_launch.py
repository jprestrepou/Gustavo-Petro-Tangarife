from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot',
            executable='nodo_motor',
            name='motor_node',
            output='screen'
        ),
        Node(
            package='robot',
            executable='nodo_led',
            name='led_node',
            output='screen'
        ),
        Node(
            package='robot',
            executable='nodo_servo',
            name='servo_node',
            output='screen'
        ),
    ])
