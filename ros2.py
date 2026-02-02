#!/usr/bin/env python3
"""
Stretch Robot Demo Node

This ROS2 node demonstrates basic functionality of the Hello Robot Stretch,
including arm control, wrist movements, gripper operation, head camera control,
and mobile base navigation.

Prerequisites:
    Launch the stretch driver first:
    ros2 launch stretch_core stretch_driver.launch.py
"""

import hello_helpers.hello_misc as hm
import numpy as np
import sys
import time


class StretchDemoNode:
    """A demonstration node for Hello Robot Stretch basic operations."""
    
    def __init__(self, node_name='stretch_demo_node'):
        """
        Initialize the Stretch Demo Node.
        
        Args:
            node_name (str): Name of the ROS2 node
        """
        self.node = hm.HelloNode.quick_create(node_name)
        self.node.get_logger().info(f'{node_name} initialized')
        
    def extend_arm_and_lift(self):
        """Extend the telescoping arm and raise the lift to maximum."""
        self.node.get_logger().info('Extending arm and lifting...')
        # Use near maximum values for arm and lift
        self.node.move_to_pose({
            'joint_arm': 0.52,  # Near maximum extension
            'joint_lift': 1.10   # Near maximum height
        }, blocking=True)
        self.node.get_logger().info('Arm extended and lift raised')
        time.sleep(2)  # Increased delay to ensure arm/lift settle before wrist moves
        
    def move_wrist_joints(self):
        """Move all three wrist motors sequentially."""
        self.node.get_logger().info('Moving wrist joints...')
        
        # Wrist yaw
        self.node.move_to_pose({'joint_wrist_yaw': np.radians(30)}, blocking=True)
        self.node.get_logger().info('Wrist yaw moved')
        time.sleep(1)
        
        # Wrist pitch
        self.node.move_to_pose({'joint_wrist_pitch': np.radians(30)}, blocking=True)
        self.node.get_logger().info('Wrist pitch moved')
        time.sleep(1)
        
        # Wrist roll
        self.node.move_to_pose({'joint_wrist_roll': np.radians(30)}, blocking=True)
        self.node.get_logger().info('Wrist roll moved')
        time.sleep(2)
        
    def operate_gripper(self):
        """Open and close the gripper."""
        self.node.get_logger().info('Operating gripper...')
        
        # Open gripper
        self.node.move_to_pose({'joint_gripper_finger_left': 100.0}, blocking=True)
        self.node.get_logger().info('Gripper opened')
        time.sleep(2)
        
        # Close gripper
        self.node.move_to_pose({'joint_gripper_finger_left': -100.0}, blocking=True)
        self.node.get_logger().info('Gripper closed')
        time.sleep(2)
        
    def move_head_camera(self):
        """Rotate the RealSense head camera motors."""
        self.node.get_logger().info('Moving head camera...')
        
        # Move head pan
        self.node.move_to_pose({'joint_head_pan': np.radians(30)}, blocking=True)
        self.node.get_logger().info('Head pan moved')
        time.sleep(1)
        
        # Move head tilt
        self.node.move_to_pose({'joint_head_tilt': np.radians(30)}, blocking=True)
        self.node.get_logger().info('Head tilt moved')
        time.sleep(1)
        
    def navigate_forward_and_back(self):
        """Drive forward, rotate 180 degrees, and return to start position."""
        self.node.get_logger().info('Starting navigation sequence...')
        
        # Drive forward 0.5 meters
        self.node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)
        self.node.get_logger().info('Moved forward 0.5m')
        time.sleep(1)
        
        # Rotate 180 degrees
        self.node.move_to_pose({'rotate_mobile_base': np.radians(180)}, blocking=True)
        self.node.get_logger().info('Rotated 180 degrees')
        time.sleep(1)
        
        # Drive forward 0.5 meters (back to start)
        self.node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)
        self.node.get_logger().info('Returned to start position')
        time.sleep(1)
        
    def run_demo(self):
        """Execute the full demonstration sequence."""
        try:
            self.node.get_logger().info('Starting Stretch robot demonstration')
            
            # Stow the robot at start
            self.node.get_logger().info('Stowing robot...')
            self.node.stow_the_robot()
            time.sleep(2)  # Wait for stow to complete
            
            # Execute demonstration sequence
            self.extend_arm_and_lift()
            self.move_wrist_joints()
            self.operate_gripper()
            self.move_head_camera()
            
            # Stow before navigation
            self.node.get_logger().info('Stowing robot before navigation...')
            self.node.stow_the_robot()
            time.sleep(1)  # Wait for stow to complete
            
            # Execute navigation
            self.navigate_forward_and_back()
            
            self.node.get_logger().info('Demonstration completed successfully')
            
        except Exception as e:
            self.node.get_logger().error(f'Error during demonstration: {str(e)}')
            raise
            
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Stop the robot and release resources."""
        self.node.get_logger().info('Cleaning up...')
        self.node.stop_the_robot()
        self.node.get_logger().info('Robot resources released')


def main():
    """Main entry point for the node."""
    try:
        demo_node = StretchDemoNode('stretch_demo_node')
        demo_node.run_demo()
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        sys.exit(0)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
