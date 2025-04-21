import math
import unittest

from VEXLib.Geometry.Rotation2d import Rotation2d


class TestRotation2d(unittest.TestCase):
    """Test basic operations"""

    def test_addition(self):
        # Test the addition of two Rotation2d objects
        r1 = Rotation2d(math.pi / 2)
        r2 = Rotation2d(math.pi / 4)
        result = r1 + r2
        self.assertAlmostEqual(result.angle_radians, math.pi * 3 / 4)

    def test_subtraction(self):
        # Test the subtraction of two Rotation2d objects
        r1 = Rotation2d(math.pi / 2)
        r2 = Rotation2d(math.pi / 4)
        result = r1 - r2
        self.assertAlmostEqual(result.angle_radians, math.pi / 4)

    def test_multiplication(self):
        # Test the multiplication of a Rotation2d object by a scalar
        r1 = Rotation2d(math.pi / 2)
        scalar = 2
        result = r1 * scalar
        self.assertAlmostEqual(result.angle_radians, math.pi)

    def test_division(self):
        # Test the division of a Rotation2d object by a scalar
        r1 = Rotation2d(math.pi / 2)
        scalar = 2
        result = r1 / scalar
        self.assertAlmostEqual(result.angle_radians, math.pi / 4)

    def test_floor_division(self):
        # Test the floor division of a Rotation2d object by a scalar
        r1 = Rotation2d(math.pi / 2)
        scalar = 0.5
        result = r1 // scalar
        self.assertAlmostEqual(result.angle_radians, 3)

    # Test comparison operations
    def test_equality(self):
        # Test the equality of two Rotation2d objects
        r1 = Rotation2d(math.pi / 2)
        r2 = Rotation2d(math.pi / 2)
        self.assertEqual(r1, r2)

    def test_comparison(self):
        # Test comparison operations between Rotation2d objects
        r1 = Rotation2d(math.pi / 2)
        r2 = Rotation2d(math.pi / 4)
        self.assertTrue(r1 > r2)
        self.assertFalse(r1 < r2)
        self.assertTrue(r1 >= r2)
        self.assertFalse(r1 <= r2)
        self.assertFalse(r1 == r2)

    """Test creation from different representations"""

    def test_from_radians(self):
        # Test creating a Rotation2d object from radians
        angle = math.pi / 2
        rotation = Rotation2d.from_radians(angle)
        self.assertAlmostEqual(rotation.angle_radians, angle)

    def test_from_degrees(self):
        # Test creating a Rotation2d object from degrees
        angle_degrees = 90
        angle_radians = math.pi / 2
        rotation = Rotation2d.from_degrees(angle_degrees)
        self.assertAlmostEqual(rotation.angle_radians, angle_radians)

    def test_from_revolutions(self):
        # Test creating a Rotation2d object from revolutions
        result = Rotation2d.from_revolutions(2.5)
        self.assertAlmostEqual(result.angle_radians, math.pi * 5)

    """Test conversion to different representations"""

    def test_to_radians(self):
        # Test converting a Rotation2d object to radians
        angle_radians = math.pi / 2
        rotation = Rotation2d(angle_radians)
        self.assertAlmostEqual(rotation.to_radians(), angle_radians)

    def test_to_degrees(self):
        # Test converting a Rotation2d object to degrees
        angle_degrees = 90
        angle_radians = math.pi / 2
        rotation = Rotation2d(angle_radians)
        self.assertAlmostEqual(rotation.to_degrees(), angle_degrees)

    def test_to_revolutions(self):
        # Test converting a Rotation2d object to revolutions
        rotation = Rotation2d(math.pi / 2)
        self.assertAlmostEqual(rotation.to_revolutions(), 0.25)

    """Test trigonometric functions"""

    def test_trigonometric_functions(self):
        # Test various trigonometric functions of Rotation2d
        functions = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "asinh": math.asinh,
        }

        # Notice that acosh and atanh are left out and tested below, this is because they have a limited input domain

        angles = [math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2]

        for func_name, math_func in functions.items():
            with self.subTest(func=func_name):
                for angle in angles:
                    rotation = Rotation2d(angle)
                    result = getattr(rotation, func_name)()
                    expected = math_func(angle)
                    self.assertAlmostEqual(
                        result, expected, msg=f"{func_name} failed for angle {angle}"
                    )

    def test_trigonometric_exceptions(self):
        # Test acosh and atanh functions which have limited input domain
        acosh_angle = math.pi / 4 + 1  # acosh is only defined for x >= 1
        atanh_angle = 0.5  # atanh is only defined for |x| < 1

        rotation_acosh = Rotation2d(acosh_angle)
        rotation_atanh = Rotation2d(atanh_angle)

        self.assertAlmostEqual(rotation_acosh.acosh(), math.acosh(acosh_angle))
        self.assertAlmostEqual(rotation_atanh.atanh(), math.atanh(atanh_angle))

    """Test interpolation and normalization"""

    def test_interpolate(self):
        # Test linear interpolation between two Rotation2d objects
        r1 = Rotation2d(math.pi / 2)
        r2 = Rotation2d(math.pi / 4)
        interpolated = r1.interpolate(r2, 0.5)
        self.assertAlmostEqual(interpolated.angle_radians, math.pi * 3 / 8)

        # Test linear interpolation with the allow_extrapolation flag
        r1 = Rotation2d(math.pi)
        r2 = Rotation2d(3 / 2 * math.pi)
        interpolated_with_extrapolation = r1.interpolate(
            r2, 3, allow_extrapolation=True
        )
        interpolated_without_extrapolation = r1.interpolate(
            r2, 3, allow_extrapolation=False
        )
        self.assertAlmostEqual(
            interpolated_with_extrapolation.angle_radians, 2.5 * math.pi
        )
        self.assertAlmostEqual(
            interpolated_without_extrapolation.angle_radians, 3 / 2 * math.pi
        )

    def test_normalize(self):
        # Test normalization of a Rotation2d object
        r1 = Rotation2d(math.pi * 3)
        normalized = r1.normalize()
        self.assertAlmostEqual(normalized.angle_radians, math.pi)


if __name__ == "__main__":
    unittest.main()
