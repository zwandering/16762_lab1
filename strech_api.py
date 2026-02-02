# 1. Move the arm and gripper back to it’s ‘stow’ position. This can be done with a singleline of code.
# 2. Extend the telescoping arm all the way out and raise the lift all the way up at thesame time. Once lifted, move all three of the wrist motors, one at a time (not all atonce). Any rotation amount is fine as long as it is visible. Then open the gripper andclose it. Then rotate both of the two motors connected to the RealSense (headcamera). Then reset everything back to the ‘stow’ position.
# 3. Once in stow, drive the robot forward 0.5 meters, rotate 180 degrees, then drive 0.5meters forward (back to the starting position).

from stretch_body.robot import Robot
import time
import math

def main():
    robot = Robot()
    robot.startup()
    
    # 1. Move the arm and gripper back to its 'stow' position (single line).
    robot.stow()
    time.sleep(3)  # Wait for stow to complete

    # 2. Extend the telescoping arm all the way out and raise the lift all the way up at the same time.
    arm_limit = robot.arm.soft_motion_limits['hard'][-1]
    lift_limit = robot.lift.soft_motion_limits['hard'][-1]
    robot.arm.move_to(arm_limit)  # Extend arm to near maximum
    robot.lift.move_to(lift_limit)  # Raise lift to near maximum
    robot.push_command()
    robot.wait_command()  # Wait for the movements to complete

    # Move wrist motors one at a time (angles in radians)
    # Wrist yaw
    robot.end_of_arm.move_to('wrist_yaw', math.radians(45))
    robot.push_command()
    robot.wait_command()
    time.sleep(1)

    # Wrist pitch
    robot.end_of_arm.move_to('wrist_pitch', math.radians(30))
    robot.push_command()
    robot.wait_command()
    time.sleep(1)
    
    # Wrist roll
    robot.end_of_arm.move_to('wrist_roll', math.radians(30))
    robot.push_command()
    robot.wait_command()
    time.sleep(2)

    # Open and close the gripper
    robot.end_of_arm.move_to('stretch_gripper', 100)  # Open
    robot.push_command()
    robot.wait_command()
    time.sleep(2)
    robot.end_of_arm.move_to('stretch_gripper', -100)  # Close
    robot.push_command()
    robot.wait_command()
    time.sleep(2)

    # Rotate both motors connected to the RealSense (head camera)
    robot.head.move_to('head_pan', math.radians(45))
    robot.push_command()
    robot.wait_command()
    time.sleep(1)
    
    robot.head.move_to('head_tilt', math.radians(45))
    robot.push_command()
    robot.wait_command()
    time.sleep(1)

    # Reset everything back to the 'stow' position
    robot.stow()
    robot.wait_command()
    time.sleep(1)  # Wait for stow to complete

    # 3. Drive the robot forward 0.5 meters, rotate 180 degrees, then drive 0.5 meters forward again.
    robot.base.translate_by(0.5)  # Move forward 0.5 meters
    robot.push_command()
    robot.wait_command()
    time.sleep(1)
    
    robot.base.rotate_by(math.pi)  # Rotate 180 degrees (pi radians)
    robot.push_command()
    robot.wait_command()
    time.sleep(1)
    
    robot.base.translate_by(0.5)  # Move forward 0.5 meters (back to start)
    robot.push_command()
    robot.wait_command()
    time.sleep(1)

    robot.stop()
    robot.shutdown()

if __name__ == "__main__":
    main()