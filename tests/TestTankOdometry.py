import unittest
from unittest.mock import MagicMock
from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Translation2d import Translation2d
from vex import Inertial
from src.Odometry import TankOdometry


class TestTankOdometry(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test environment before each test runs.
        A mocked inertial sensor is used for controlled scenarios.
        """
        # Create a new mock object to simulate the inertial sensor
        self.mock_inertial = MagicMock(spec=Inertial)
        self.mock_inertial.rotation.return_value = 0  # Default mock value for sensor rotation

        # Initialize a fresh TankOdometry object for each test
        self.odometry = TankOdometry(self.mock_inertial)

    def test_initialization(self):
        """
        Tests that TankOdometry initializes with appropriate default values.
        """
        self.assertIsInstance(self.odometry.get_pose(), Pose2d)
        self.assertIsInstance(self.odometry.get_translation(), Translation2d)
        self.assertIsInstance(self.odometry.get_rotation(), Rotation2d)

        # Verify initial values
        self.assertEqual(self.odometry.get_translation().x_component.to_meters(), 0)
        self.assertEqual(self.odometry.get_translation().y_component.to_meters(), 0)
        self.assertEqual(self.odometry.get_rotation().to_degrees(), 0)

    def test_update_pose_with_no_rotation(self):
        """
        Tests pose updates when there is no rotation (straight-line movement).
        """
        # Simulate straight-line movement: left and right wheels move equally
        left_position = Distance.from_meters(1.0)
        right_position = Distance.from_meters(1.0)
        self.mock_inertial.rotation.return_value = 0  # Inertial sensor reports 0 degrees

        # Update odometry
        self.odometry.update(left_position, right_position)

        # Expected values: forward movement without rotation
        expected_x = 1.0  # Forward by 1 meter
        expected_y = 0.0
        expected_rotation = 0.0  # No rotation

        # Assertions
        self.assertAlmostEqual(self.odometry.get_translation().x_component.to_meters(), expected_x, places=5)
        self.assertAlmostEqual(self.odometry.get_translation().y_component.to_meters(), expected_y, places=5)
        self.assertAlmostEqual(self.odometry.get_rotation().to_degrees(), expected_rotation, places=5)

    def test_update_pose_with_rotation(self):
        """
        Tests pose updates when there is rotation and translation.
        """
        # Simulate movement: left and right wheels move equally 1 meter
        left_position = Distance.from_meters(1.0)
        right_position = Distance.from_meters(1.0)
        self.mock_inertial.rotation.return_value = 90  # Clockwise-positive (90 degrees)

        # Update odometry
        self.odometry.update(left_position, right_position)

        # Expected values for 90-degree rotation:
        expected_x = 0.0  # No movement along the x-axis
        expected_y = 1.0  # Forward along the y-axis
        expected_rotation = 90.0  # Converted to counterclockwise-positive internally

        # Assertions
        self.assertAlmostEqual(self.odometry.get_translation().x_component.to_meters(), expected_x, places=5)
        self.assertAlmostEqual(self.odometry.get_translation().y_component.to_meters(), expected_y, places=5)
        self.assertAlmostEqual(self.odometry.get_rotation().to_degrees(), expected_rotation, places=5)

    def test_update_pose_with_rotation_at_45_degrees(self):
        """
        Tests pose updates when the robot is at a 45-degree orientation.
        """
        # Simulate movement: left and right wheels move equally 1 meter
        left_position = Distance.from_meters(1.0)
        right_position = Distance.from_meters(1.0)
        self.mock_inertial.rotation.return_value = -45  # Clockwise +45 degrees from inertial sensor

        # Update odometry
        self.odometry.update(left_position, right_position)

        # Expected values:
        expected_x = 1.0 / (2 ** 0.5)  # cos(45) * forward distance (sqrt(2)/2)
        expected_y = -1.0 / (2 ** 0.5)  # sin(45) * forward distance (sqrt(2)/2), negative due to rotation
        expected_rotation = -45.0  # Counterclockwise-positive

        # Assertions
        self.assertAlmostEqual(self.odometry.get_translation().x_component.to_meters(), expected_x, places=5)
        self.assertAlmostEqual(self.odometry.get_translation().y_component.to_meters(), expected_y, places=5)
        self.assertAlmostEqual(self.odometry.get_rotation().to_degrees(), expected_rotation, places=5)

    def test_update_pose_with_backwards_movement(self):
        """
        Tests pose updates when the robot moves backward.
        """
        # Simulate backward movement
        left_position = Distance.from_meters(-1.0)
        right_position = Distance.from_meters(-1.0)
        self.mock_inertial.rotation.return_value = 0  # No rotation

        # Update odometry
        self.odometry.update(left_position, right_position)

        # Expected values: backward 1 meter
        expected_x = -1.0  # Negative x indicates backward movement
        expected_y = 0.0
        expected_rotation = 0.0  # No rotation

        # Assertions
        self.assertAlmostEqual(self.odometry.get_translation().x_component.to_meters(), expected_x, places=5)
        self.assertAlmostEqual(self.odometry.get_translation().y_component.to_meters(), expected_y, places=5)
        self.assertAlmostEqual(self.odometry.get_rotation().to_degrees(), expected_rotation, places=5)

    def test_reset_pose(self):
        """
        Tests the reset functionality of the pose.
        """
        # Simulate some movement
        self.odometry.update(Distance.from_meters(1.0), Distance.from_meters(1.0))

        # Reset pose to a defined value
        new_pose = Pose2d(
            Translation2d(Distance.from_meters(2.0), Distance.from_meters(3.0)),
            Rotation2d.from_degrees(90)
        )
        self.odometry.pose = new_pose

        # Check if reset values match
        self.assertEqual(self.odometry.get_translation().x_component.to_meters(), 2.0)
        self.assertEqual(self.odometry.get_translation().y_component.to_meters(), 3.0)
        self.assertEqual(self.odometry.get_rotation().to_degrees(), 90.0)


if __name__ == '__main__':
    unittest.main()
