import unittest
from unittest.mock import MagicMock

from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Kinematics.TankOdometry import TankOdometry
from vex import Inertial

mock_inertial = MagicMock(spec=Inertial)
mock_inertial.rotation.return_value = 0
odometry = TankOdometry(mock_inertial, Rotation2d.from_degrees(0))


class TestTankOdometry(unittest.TestCase):
    def setUp(self):
        global odometry, mock_inertial
        mock_inertial.rotation.return_value = 0
        odometry = TankOdometry(mock_inertial, Rotation2d.from_degrees(0))

    def assertPoseAlmostEqual(self, pose1, pose2, delta=1e-6):
        self.assertAlmostEqual(
            pose1.translation.x_component.to_meters(),
            pose2.translation.x_component.to_meters(),
            delta=delta,
        )
        self.assertAlmostEqual(
            pose1.translation.y_component.to_meters(),
            pose2.translation.y_component.to_meters(),
            delta=delta,
        )
        self.assertAlmostEqual(
            pose1.rotation.to_degrees(), pose2.rotation.to_degrees(), delta=delta
        )

    def test_update_pose_with_backwards_movement(self):
        odometry.update(Distance.from_meters(-1.0), Distance.from_meters(-1.0))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(-1.0, 0.0), Rotation2d.from_degrees(0)),
        )

    def test_update_pose_with_no_movement(self):
        odometry.update(Distance.from_meters(0), Distance.from_meters(0))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(0.0, 0.0), Rotation2d.from_degrees(0)),
        )

    def test_update_pose_with_opposite_wheel_movement(self):
        odometry.update(Distance.from_meters(-1.0), Distance.from_meters(1.0))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(0.0, 0.0), Rotation2d.from_degrees(0)),
        )

    def test_update_pose_with_forward_movement(self):
        odometry.update(Distance.from_meters(3.0), Distance.from_meters(3.0))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(3.0, 0.0), Rotation2d.from_degrees(0)),
        )

    def test_update_pose_with_rotation(self):
        mock_inertial.rotation.return_value = 90
        odometry.update(Distance.from_meters(3.0), Distance.from_meters(3.0))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(0.0, 3.0), Rotation2d.from_degrees(90)),
        )

    # Edge case: very small movements
    def test_update_pose_with_very_small_movement(self):
        odometry.update(Distance.from_meters(1e-5), Distance.from_meters(1e-5))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(1e-5, 0.0), Rotation2d.from_degrees(0)),
        )

    # Edge case: very large movements
    def test_update_pose_with_very_large_movement(self):
        odometry.update(Distance.from_meters(1e6), Distance.from_meters(1e6))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(1e6, 0.0), Rotation2d.from_degrees(0)),
            delta=5,
        )  # Allow a larger delta for the very large movement

    # Error case: negative distance
    def test_update_pose_with_negative_distance(self):
        odometry.update(Distance.from_meters(-1e6), Distance.from_meters(-1e6))
        self.assertPoseAlmostEqual(
            odometry.get_pose(),
            Pose2d(Translation2d.from_meters(-1e6, 0.0), Rotation2d.from_degrees(0)),
        )  # Allow a larger delta for the very large movement


if __name__ == "__main__":
    unittest.main()
