import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import argparse
import sys
import time

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import world_object_pb2
from bosdyn.api.geometry_pb2 import Vec2
from bosdyn.client import math_helpers
from bosdyn.client.frame_helpers import get_vision_tform_body
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.world_object import (WorldObjectClient, make_add_world_object_req, make_delete_world_object_req, send_add_mutation_requests, send_delete_mutation_requests)
from bosdyn.util import seconds_to_duration

from bosdyn.client import create_standard_sdk
from bosdyn.client.robot import Robot
from bosdyn.client.util import authenticate

class SpotBodyObstacleNode(Node):
	def __init__(self):
		super().__init__('spot_world_objects')
		self.get_logger().info("Connecting to Spot robot")
		# Declare ROS2 publisher		
		# Connect to Spot
		self.sdk = bosdyn.client.create_standard_sdk('WorldObjectsClient')
		self.robot = self.sdk.create_robot("192.168.50.3")
		bosdyn.client.util.authenticate(self.robot)
		
		self.robot.time_sync.wait_for_sync()
		self.world_object_client = self.robot.ensure_client(WorldObjectClient.default_service_name)
		if self.world_object_client is None:
			self.get_logger().error("world_object_client is not initialized")
		self.robot_state_client = self.robot.ensure_client(RobotStateClient.default_service_name)
		
		self.robot_state = self.robot_state_client.get_robot_state()
		self.vision_T_body = get_vision_tform_body(self.robot_state.kinematic_state.transforms_snapshot)
		
		self.body_T_obs0 = math_helpers.SE3Pose(x=1.0, y=0.0, z=0, rot=math_helpers.Quat())
		self.vis_T_obs0 = self.vision_T_body * self.body_T_obs0
		
		# Creating body obstacle box
		self.obs = world_object_pb2.WorldObject(name='obstacle', object_lifetime=seconds_to_duration(315576000000))
		self.obs.nogo_region_properties.disable_foot_obstacle_generation = False
		self.obs.nogo_region_properties.disable_body_obstacle_generation = False
		self.obs.nogo_region_properties.disable_foot_obstacle_inflation = False
		self.obs.nogo_region_properties.box.frame_name = "vision"
		self.obs.nogo_region_properties.box.box.size.CopyFrom(Vec2(x=1, y=1))
		self.obs.nogo_region_properties.box.frame_name_tform_box.CopyFrom(self.vis_T_obs0.to_proto())
		
		self.obstacles = [self.obs]
		self.object_ids = send_add_mutation_requests(self.world_object_client, self.obstacles)
		
		self.get_logger().info("Obstacle Created")

			
def main(args=None): 
	rclpy.init(args=args)
	node = SpotBodyObstacleNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main() 
