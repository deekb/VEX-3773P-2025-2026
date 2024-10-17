from VEXLib.Math.MathUtil import smallest_angular_difference
import unittest
import math


class TestCalculateOptimalTurn(unittest.TestCase):
    def setUp(self):
        self.setpoint = 0

    def test_zero_heading(self):
        self.setpoint = 0
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, 0), 0)

    def test_positive_heading(self):
        self.setpoint = 0
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, math.pi / 2), math.pi / 2)

    def test_negative_heading(self):
        self.setpoint = 0
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, -math.pi / 2), -math.pi / 2)

    def test_large_positive_heading(self):
        self.setpoint = 0
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, 3 * math.pi), math.pi)

    def test_large_negative_heading(self):
        self.setpoint = 0
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, -3 * math.pi), math.pi)

    def test_heading_wraparound(self):
        self.setpoint = math.pi
        self.assertAlmostEqual(smallest_angular_difference(self.setpoint, 0), -math.pi)

if __name__ == '__main__':
    unittest.main()
