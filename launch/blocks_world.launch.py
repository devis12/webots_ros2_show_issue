import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher


def generate_launch_description():
    package_dir = get_package_share_directory('webots_ros2_show_issue')
    gantry_robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'gantry_robot.urdf')).read_text()
    robot2_description = pathlib.Path(os.path.join(package_dir, 'resource', 'my_simple_robot2.urdf')).read_text()

    
    
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'blocksworld.wbt')
    )

    gantry_robot_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        name='gantry_driver',
        output='screen',
        parameters=[
            {'webots_robot_name': 'gantry'},
            {'robot_description': gantry_robot_description},
        ]
    )
    
    my_robot2_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        parameters=[
            {'webots_robot_name': 'my_simple_robot2'},
            {'robot_description': robot2_description},
        ]
    )

    return LaunchDescription([
        webots,
        gantry_robot_driver,
        my_robot2_driver,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])