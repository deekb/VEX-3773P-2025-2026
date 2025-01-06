import math
import unittest

import VEXLib.Math.MathUtil as MathUtil


class TestMathUtil(unittest.TestCase):

    def test_sign(self):
        self.assertEqual(MathUtil.sign(5), 1)
        self.assertEqual(MathUtil.sign(-5), -1)
        self.assertEqual(MathUtil.sign(0), 1)
        self.assertEqual(MathUtil.sign(-0), 1)

    def test_average(self):
        self.assertAlmostEqual(MathUtil.average(1, 2, 3), 2.0)
        self.assertAlmostEqual(MathUtil.average(5, 10), 7.5)
        self.assertAlmostEqual(MathUtil.average(3.5, 4.5, 6.0), 4.666666666666667)
        self.assertAlmostEqual(MathUtil.average_iterable([1, 2, 3]), 2.0)
        self.assertRaises(TypeError, MathUtil.average, [1, 2, 3])

    def test_clamp(self):
        self.assertEqual(MathUtil.clamp(5, 0, 10), 5)
        self.assertEqual(MathUtil.clamp(-1, 0, 10), 0)
        self.assertEqual(MathUtil.clamp(15, 0, 10), 10)
        self.assertEqual(MathUtil.clamp(5, None, 10), 5)
        self.assertEqual(MathUtil.clamp(15, None, 10), 10)
        self.assertEqual(MathUtil.clamp(5, 0, None), 5)
        self.assertEqual(MathUtil.clamp(-5, 0, None), 0)
        self.assertRaises(ValueError, MathUtil.clamp, 5, 10, 0)

    def test_apply_deadband(self):
        self.assertAlmostEqual(MathUtil.apply_deadband(0.1, 0.2, 1.0), 0.0, 6)
        self.assertAlmostEqual(MathUtil.apply_deadband(0.3, 0.2, 1.0), 0.125, 6)
        self.assertAlmostEqual(MathUtil.apply_deadband(-0.3, 0.2, 1.0), -0.125, 6)
        self.assertAlmostEqual(MathUtil.apply_deadband(0.3, 0.2, 10.0), 0.1020408, 6)
        self.assertAlmostEqual(MathUtil.apply_deadband(-0.3, 0.2, 10.0), -0.1020408, 6)

    def test_input_modulus(self):
        self.assertEqual(MathUtil.input_modulus(5, 0, 10), 5)
        self.assertEqual(MathUtil.input_modulus(15, 0, 10), 5)
        self.assertEqual(MathUtil.input_modulus(-5, 0, 10), 5)
        self.assertEqual(MathUtil.input_modulus(25, 0, 10), 5)

    def test_angle_modulus(self):
        self.assertAlmostEqual(MathUtil.angle_modulus(math.pi), math.pi)
        self.assertAlmostEqual(MathUtil.angle_modulus(-math.pi), math.pi)
        self.assertAlmostEqual(MathUtil.angle_modulus(3 * math.pi), math.pi)
        self.assertAlmostEqual(MathUtil.angle_modulus(-3 * math.pi), math.pi)

    def test_interpolate(self):
        self.assertAlmostEqual(MathUtil.interpolate(0, 10, 0.5), 5.0)
        self.assertAlmostEqual(MathUtil.interpolate(0, 10, 1.5), 15.0)
        self.assertAlmostEqual(MathUtil.interpolate(0, 10, -0.5), -5)
        self.assertAlmostEqual(MathUtil.interpolate(0, 10, 1.5, allow_extrapolation=False), 10.0)
        self.assertAlmostEqual(MathUtil.interpolate(0, 10, -0.5, allow_extrapolation=False), 0.0)

    def test_interpolate_2d(self):
        # Test with extrapolation allowed
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, 5), 5.0)
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, -5), -5.0)
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, 15), 15.0)

        # Test with extrapolation disallowed
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, 5, allow_extrapolation=False), 5.0)
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, -5, allow_extrapolation=False), 0.0)
        self.assertAlmostEqual(MathUtil.interpolate_2d(0, 10, 0, 10, 15, allow_extrapolation=False), 10.0)

    def test_inverse_interpolate(self):
        # Test with extrapolation allowed
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, 5), 0.5)
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, -5), 0.0)
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, 15), 1.0)

        # Test with extrapolation disallowed
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, 5, allow_extrapolation=False), 0.5)
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, -5, allow_extrapolation=False), 0.0)
        self.assertAlmostEqual(MathUtil.inverse_interpolate(0, 10, 15, allow_extrapolation=False), 1.0)

    def test_is_near(self):
        self.assertTrue(MathUtil.is_near(5.0, 5.1, 0.2))
        self.assertFalse(MathUtil.is_near(5.0, 5.3, 0.2))
        self.assertRaises(ValueError, MathUtil.is_near, 5.0, 5.1, -0.2)

    def test_is_near_continuous(self):
        self.assertTrue(MathUtil.is_near_continuous(2, 359, 5, 0, 360))
        self.assertFalse(MathUtil.is_near_continuous(2, 350, 5, 0, 360))
        self.assertRaises(ValueError, MathUtil.is_near_continuous, 2, 359, -5, 0, 360)

    def test_cubic_filter(self):
        self.assertAlmostEqual(MathUtil.cubic_filter(0.5, 0), 0.125)
        self.assertAlmostEqual(MathUtil.cubic_filter(0.5, 1), 0.5)
        self.assertAlmostEqual(MathUtil.cubic_filter(-0.5, 0), -0.125)
        self.assertRaises(ValueError, MathUtil.cubic_filter, 1.5, 0)
        self.assertRaises(ValueError, MathUtil.cubic_filter, 0.5, 1.5)

    def test_distance_from_point_to_line(self):
        self.assertAlmostEqual(MathUtil.distance_from_point_to_line((0, 0), 1, 0), 0.0)
        self.assertAlmostEqual(MathUtil.distance_from_point_to_line((1, 1), -1, 0), math.sqrt(2))
        self.assertAlmostEqual(MathUtil.distance_from_point_to_line((1, 1), math.inf, 1), 1.0)

    def test_factorial(self):
        self.assertEqual(MathUtil.factorial(0), 1)
        self.assertEqual(MathUtil.factorial(5), 120)
        self.assertEqual(MathUtil.factorial(10), 3628800)

    def test_sin(self):
        self.assertAlmostEqual(MathUtil.sin(math.pi / 2), 1.0, places=5)
        self.assertAlmostEqual(MathUtil.sin(math.pi), 0.0, places=5)
        self.assertAlmostEqual(MathUtil.sin(3 * math.pi / 2), -1.0, places=5)
        self.assertAlmostEqual(MathUtil.sin(2 * math.pi), 0.0, places=5)

    def test_average_edge_cases(self):
        self.assertRaises(ZeroDivisionError, MathUtil.average)  # No arguments should return 0
        self.assertAlmostEqual(MathUtil.average(1), 1.0)  # Single value should return the value itself
        self.assertAlmostEqual(MathUtil.average(1, 1, 1, 1), 1.0)  # All values are the same

    def test_apply_deadband_edge_cases(self):
        self.assertRaises(ValueError, MathUtil.apply_deadband, 0.5, 0.2, 0.1)  # Deadband smaller than input
        self.assertAlmostEqual(MathUtil.apply_deadband(0.1, 0.1, 0.2), 0.0, 6)  # Deadband equal to input
        self.assertAlmostEqual(MathUtil.apply_deadband(0.1, 0.2, 0.2), 0.0, 6)  # Deadband larger than input

    def test_input_modulus_edge_cases(self):
        self.assertEqual(MathUtil.input_modulus(5, 10, 20), 15)
        self.assertEqual(MathUtil.input_modulus(25, 10, 20), 15)

    def test_clamp_edge_cases(self):
        self.assertEqual(MathUtil.clamp(5, 10, 20), 10)
        self.assertEqual(MathUtil.clamp(25, 10, 20), 20)



if __name__ == '__main__':
    unittest.main()
