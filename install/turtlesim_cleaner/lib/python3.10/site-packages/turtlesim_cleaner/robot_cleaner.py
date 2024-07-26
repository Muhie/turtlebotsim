#!/usr/bin/env python
#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import numpy as np
import time
import sys
# Muhie
# 25/07/24
""""A program that allows a player to enter a target point 
and then the turtle will try to get to it using some simple maths
this is just to get familiar with the ros publisher and subscriber architechure
this is based off the ros guide: https://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal"""

class Driver_Node(Node):
    def __init__(self):
        super().__init__('driving_custom_Node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
        self.timer = self.create_timer(0.1, self.move_to_goal)
        self.pose = Pose()


    def update_pose(self, data):
        """A callback method that is called when a new 
        message with the type Pose is recieved by the subscriber"""
        self.pose = data

    def move_to_goal(self):
        """ A method that moves toward the goal when 3 values are passed to it"""

        goal = Pose()
        goal.x = float(sys.argv[1])
        goal.y = float(sys.argv[2])
        goal.theta = float(sys.argv[3])

        new_vel = Twist()

        distance_to_goal = math.sqrt((goal.x - self.pose.x)**2 + (goal.y - self.pose.y)**2)

        angle_to_goal = math.atan2(goal.y - self.pose.y, goal.x - self.pose.x)

        distance_tolerance = 0.1
        angle_tolerance = 0.01

        angle_error = angle_to_goal - self.pose.theta

        kp = 1.4

        if abs(angle_error) > angle_tolerance:
            new_vel.angular.z = kp * angle_error
        else:
            if (distance_to_goal) >= distance_tolerance:
                new_vel.linear.x = kp * distance_to_goal
            else:
                new_vel.linear.x = 0.0
                self.get_logger().info("goal reached")
                quit()

        self.publisher_.publish(new_vel)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Driver_Node()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()