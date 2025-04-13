import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
import numpy as np
import cv2
class FiducialFilterNodeBack(Node):
	def __init__(self):
		super().__init__('fiducial_filter_node_back')
		# Camera topic to filter
		self.camera_topic = "/spot1/camera/back/compressed"
		self.filtered_camera_topic = "/spot1/camera/back/filtered"
		# Store the most recent list of blocked cameras
		self.blocked_cameras = set()
		# Subscribers
		self.world_objects_sub = self.create_subscription(String, "/spot/world_objects", self.world_objects_callback, 10)
		self.camera_sub = self.create_subscription(CompressedImage, self.camera_topic, self.camera_callback, 10)
		# Publisher
		self.camera_pub = self.create_publisher(CompressedImage, self.filtered_camera_topic, 10)
	def world_objects_callback(self, msg):
		""" Updates the blocked cameras list from world objects """
		# self.get_logger().info(f"Received world objects: {msg.data}")
		# Parse the message to extract camera names
		self.blocked_cameras = set(msg.data.split(', '))
	def camera_callback(self, msg):
		""" Publishes the image only if the camera is NOT blocked """
		camera_name = "back" # Adjust according to world objects format
		if camera_name in self.blocked_cameras:
			# self.get_logger().info(f"Blocking camera: {camera_name}")
			# Option 1: Do not publish
			# return
			# Option 2: Publish a black frame (uncomment to use this)
			msg.data = self.create_black_frame(msg)
			self.camera_pub.publish(msg)
		else:
			# self.get_logger().info(f"Publishing from: {camera_name}")
			self.camera_pub.publish(msg)
	def create_black_frame(self, msg):
		""" Generates a black frame with the same size as the original image """
		np_arr = np.frombuffer(msg.data, np.uint8)
		img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
		if img is not None:
			black_img = np.zeros_like(img)
			_, black_encoded = cv2.imencode('.jpg', black_img)
			return black_encoded.tobytes()
		return msg.data # Fallback: if decoding fails, return original
def main(args=None):
	rclpy.init(args=args)
	node = FiducialFilterNodeBack()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
