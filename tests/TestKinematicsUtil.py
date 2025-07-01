import math
import unittest
from math import cos, sin
from unittest.mock import MagicMock

from VEXLib.Geometry.Pose2d import Pose2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Distance
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Kinematics import GenericOdometry
from vex import Inertial


class TestGenericOdometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_inertial_sensor = MagicMock(spec=Inertial)
        cls.mock_inertial_sensor.rotation.return_value = 0
        cls.wheel_directions = [Rotation2d.from_degrees(0), Rotation2d.from_degrees(0)]

    def setUp(self):
        self.odometry = GenericOdometry(self.mock_inertial_sensor, self.wheel_directions)
        self.odometry.update([Distance(0)] * len(self.wheel_directions))
        self.mock_inertial_sensor.rotation.return_value = 0

    def assertPoseAlmostEqual(self, pose1, pose2, delta=1e-6):
        self.assertAlmostEqual(pose1.translation.x_component.to_meters(), pose2.translation.x_component.to_meters(), delta=delta)
        self.assertAlmostEqual(pose1.translation.y_component.to_meters(), pose2.translation.y_component.to_meters(), delta=delta)
        self.assertAlmostEqual(pose1.rotation.to_revolutions(), pose2.rotation.to_revolutions(), delta=delta)

    def test_initial_pose(self):
        self.assertEqual(self.odometry.pose, Pose2d())

    def test_update_pose(self):
        self._update_and_assert_pose([1, 1], Pose2d(Translation2d.from_meters(1, 0), Rotation2d()))

    def test_get_translation(self):
        self._update_and_assert_translation([1, 1], Translation2d.from_meters(1, 0))

    def test_get_rotation(self):
        self.mock_inertial_sensor.rotation.return_value = 90
        self.odometry.update([Distance(0), Distance(0)])
        self.assertEqual(self.odometry.get_rotation(), Rotation2d.from_degrees(90))

    def test_update_pose_with_various_movements(self):
        test_cases = [
            ([-1, -1], Pose2d(Translation2d.from_meters(-1, 0), Rotation2d())),
            ([0, 0], Pose2d(Translation2d.from_meters(0, 0), Rotation2d())),
            ([-1, 1], Pose2d(Translation2d.from_meters(0, 0), Rotation2d())),
            ([3, 3], Pose2d(Translation2d.from_meters(3, 0), Rotation2d())),
        ]
        for wheel_positions, expected_pose in test_cases:
            with self.subTest(wheel_positions=wheel_positions):
                self._update_and_assert_pose(wheel_positions, expected_pose)

    def test_update_pose_with_rotation(self):
        self.mock_inertial_sensor.rotation.return_value = 90
        self._update_and_assert_pose([3, 3], Pose2d(Translation2d.from_meters(0, 3), Rotation2d.from_degrees(90)))

    def test_update_pose_with_all_angles(self):
        for angle in range(-360, 361):  # Test all angles from -360 to 360
            expected_pose = Pose2d(
                Translation2d.from_meters(cos(math.radians(angle)), sin(math.radians(angle))),
                Rotation2d.from_degrees(angle)
            )
            self.setUp()
            self.mock_inertial_sensor.rotation.return_value = angle
            self._update_and_assert_pose([1, 1], expected_pose)

    def test_update_pose_with_all_angles_backwards(self):
        for angle in range(-360, 361):  # Test all angles from -360 to 360
            expected_pose = Pose2d(
                Translation2d.from_meters(cos(math.radians(angle)), sin(math.radians(angle))).inverse(),
                Rotation2d.from_degrees(angle)
            )
            self.setUp()
            self.mock_inertial_sensor.rotation.return_value = angle
            self._update_and_assert_pose([-1, -1], expected_pose)

    def test_update_pose_with_extreme_movements(self):
        test_cases = [
            ([1e-5, 1e-5], Pose2d(Translation2d.from_meters(1e-5, 0), Rotation2d())),
            ([1e6, 1e6], Pose2d(Translation2d.from_meters(1e6, 0), Rotation2d())),
            ([-1e6, -1e6], Pose2d(Translation2d.from_meters(-1e6, 0), Rotation2d())),
        ]
        for wheel_positions, expected_pose in test_cases:
            with self.subTest(wheel_positions=wheel_positions):
                self._update_and_assert_pose(wheel_positions, expected_pose, delta=5 if 1e6 in wheel_positions else 1e-6)

    def _update_and_assert_pose(self, wheel_positions, expected_pose, delta=1e-6):
        self.odometry.update([Distance.from_meters(pos) for pos in wheel_positions])
        self.assertPoseAlmostEqual(self.odometry.pose, expected_pose, delta=delta)

    def _update_and_assert_translation(self, wheel_positions, expected_translation):
        self.odometry.update([Distance.from_meters(pos) for pos in wheel_positions])
        self.assertEqual(self.odometry.get_translation(), expected_translation)


if __name__ == '__main__':
    unittest.main()
