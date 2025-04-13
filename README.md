fiducial_blocker folder contains code to publish "blacked-out" images whenever a fiducial is spotted. Also creates a "no-go" zone 1 meter in front of Spot that the robot cannot approach.

Add this to the src folder within a ROS workspace. Run "colcon build --packages-select fiducial_blocker --symlink-install" and "source install/local_setup.bash".

Can run with "ros2 launch fiducial_blocker fiducial_blocker_launch.py".
