import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import argparse
import sys
import time

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import world_object_pb2
from bosdyn.client.world_object import WorldObjectClient

from bosdyn.client import create_standard_sdk
from bosdyn.client.robot import Robot
from bosdyn.client.util import authenticate

from geometry_msgs.msg import Point

class SpotWorldObjectsNode(Node):
	def __init__(self):
		super().__init__('spot_world_objects')
		self.get_logger().info("Connecting to Spot robot")
		
		# Declare ROS2 publisher
		self.world_objects_publisher = self.create_publisher(String, 'spot/world_objects', 10)
		
		# Connect to Spot
		self.sdk = bosdyn.client.create_standard_sdk('WorldObjectsClient')
		self.robot = self.sdk.create_robot("192.168.50.3")
		bosdyn.client.util.authenticate(self.robot)
		
		self.robot.time_sync.wait_for_sync()
		self.world_object_client = self.robot.ensure_client(WorldObjectClient.default_service_name)
		if self.world_object_client is None:
			self.get_logger().error("world_object_client is not initialized")
		
		# Timer to periodically fetch world objects
		self.timer = self.create_timer(0.25, self.fetch_and_publish_world_objects)
		self.get_logger().info("Connected")
		
	def fetch_and_publish_world_objects(self):
		try:			
			request_fiducials = [world_object_pb2.WORLD_OBJECT_APRILTAG]
			# request_nogos = [world_object_pb2.WORLD_OBJECT_USER_NOGO]
			fiducial_objects = self.world_object_client.list_world_objects(object_type=request_fiducials).world_objects
			# self.get_logger().info(f"Objects: {fiducial_objects}")

			parent_frames = set()
			for obj in fiducial_objects:
				if hasattr(obj, "transforms_snapshot"):
					for key, transform in obj.transforms_snapshot.child_to_parent_edge_map.items():
						if transform.parent_frame_name in ["frontright", "frontleft", "right", "left", "back"]:
							parent_frames.add(transform.parent_frame_name)
	

			msg = String()
			msg.data = ", ".join(parent_frames)
			self.world_objects_publisher.publish(msg)
		
		except Exception as e:
			self.get_logger().error(f"Failed to fetch world objects: {type(e).__name__}: {e}")
			
def main(args=None): 
	rclpy.init(args=args)
	node = SpotWorldObjectsNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main() 
