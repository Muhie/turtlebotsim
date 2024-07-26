#!/usr/bin/env python
#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import numpy as np
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
        self.timer = self.create_timer(1, self.move_to_goal)
        self.pose = Pose()

    def update_pose(self, data):
        """A callback method that is called when a new 
        message with the type Pose is recieved by the subscriber"""
        self.pose = data
        self.pose_x = round(self.pose, 4)
        self.pose_y = round(self.pose, 4)

    def euclidean_distance(self, goal_pose):
        """A method that calculates the euclidean 
        distance between the curent and the goal pose"""
        return sqrt((goal_pose.x - self.pose.x)**2 
                    + (goal_pose.y - self.pose.y)**2)
    
    def linear_vel(self, goal_pose, constant=1.5):
        """Moving faster when further away and slower when closer to the target pose"""
        return constant * self.euclidean_distance(goal_pose)
    
    def steering_angle(self, goal_pose):
        """again just using simple trig here"""
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.y)
    
    def angular_vel(self, goal_pose, constant = 6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)
    
    def move_to_goal(self):
        """A method to move the turtle to the goal position"""

        goal_pose = Pose()

        # get the goal position from the user

        goal_pose.x = float(input("please enter the target x coordinate that the turtle needs to move toward: "))
        goal_pose.y = float(input("please enter the target y coordinate that the turtle needs to move toward: "))

        distance_tolerance = input("set your tolerance")

        vel_msg = Twist()


    def move_to_goal(self):
        """A method to move the turtle to the goal position"""

        goal_pose = Pose()

        # get the goal position from the user

        goal_pose.x = float(input("please enter the target x coordinate that the turtle needs to move toward: "))
        goal_pose.y = float(input("please enter the target y coordinate that the turtle needs to move toward: "))

        distance_tolerance = float(input("set your tolerance: "))
        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) > distance_tolerance:
            # proportional control
            #  Linear velocity in the x direction
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0

            # angular velocity in the z axis (rotational velocity of the turtle)

            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # publishing vel message

            self.publisher_.publish(vel_msg)

            # publish at desired rate


        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.0
        self.publisher_.publish(vel_msg)

        # Allows us to stop the program with control c


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = Driver_Node()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()