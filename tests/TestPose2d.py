import unittest
import math
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Pose2d import Pose2d


class TestPose2d(unittest.TestCase):
    def test_addition(self):
        p1 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        p2 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d(math.pi / 4))
        result = p1 + p2
        self.assertEqual(result.translation.to_meters(), (4, 6))
        self.assertAlmostEqual(result.rotation.angle_radians, math.pi * 3 / 4)

    def test_subtraction(self):
        p1 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        p2 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d(math.pi / 4))
        result = p1 - p2
        self.assertEqual(result.translation.to_meters(), (-2, -2))
        self.assertAlmostEqual(result.rotation.angle_radians, math.pi / 4)

    def test_equality(self):
        p1 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        p2 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        self.assertEqual(p1, p2)

    def test_inequality(self):
        p1 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        p2 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d(math.pi / 4))
        self.assertNotEqual(p1, p2)

    def test_multiplication(self):
        p1 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d(math.pi / 2))
        scalar = 2
        result = p1 * scalar
        self.assertEqual(result.translation.to_meters(), (2, 4))
        self.assertAlmostEqual(result.rotation.angle_radians, math.pi)

    def test_from_zero(self):
        result = Pose2d.from_zero()
        self.assertEqual(result.translation.to_meters(), (0, 0))
        self.assertEqual(result.rotation.angle_radians, 0)

    def test_from_translation2d(self):
        translation = Translation2d.from_meters(5, 10)
        result = Pose2d.from_translation2d(translation)
        self.assertEqual(result.translation.to_meters(), (5, 10))
        self.assertEqual(result.rotation.angle_radians, 0)

    def test_from_rotation2d(self):
        rotation = Rotation2d(math.pi)
        result = Pose2d.from_rotation2d(rotation)
        self.assertEqual(result.translation.to_meters(), (0, 0))
        self.assertAlmostEqual(result.rotation.angle_radians, math.pi)

    def test_of(self):
        translation = Translation2d.from_meters(7, 14)
        rotation = Rotation2d(math.pi / 3)
        result = Pose2d.of(translation, rotation)
        self.assertEqual(result.translation.to_meters(), (7, 14))
        self.assertAlmostEqual(result.rotation.angle_radians, math.pi / 3)

    def test_str(self):
        translation = Translation2d.from_meters(3, 4)
        rotation = Rotation2d(math.pi / 2)
        pose = Pose2d(translation, rotation)
        self.assertEqual(str(pose), f"Translation: {translation}, Rotation: {rotation}")

if __name__ == '__main__':
    unittest.main()
