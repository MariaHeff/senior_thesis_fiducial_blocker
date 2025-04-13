from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	return LaunchDescription([
		Node(
			package='fiducial_blocker',
			executable='detect_fiducials',
			name='detect_fiducials'
		),
		Node(
			package='fiducial_blocker',
			executable='fiducial_filter_frontright',
			name='filter_frontright'
		),
		Node(
			package='fiducial_blocker',
			executable='fiducial_filter_frontleft',
			name='filter_frontleft'
		),
		Node(
			package='fiducial_blocker',
			executable='fiducial_filter_right',
			name='filter_right'
		),
		Node(
			package='fiducial_blocker',
			executable='fiducial_filter_left',
			name='filter_left'
		),
		Node(
			package='fiducial_blocker',
			executable='fiducial_filter_back',
			name='filter_back'
		),
		Node(
			package='fiducial_blocker',
			executable='body_obstacle',
			name='body_obstacle'
		)
	])
