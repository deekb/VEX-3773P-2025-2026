import unittest
from VEXLib.Geometry.Velocity1d import Velocity1d, Speed

class TestVelocity1d(unittest.TestCase):
    def test_addition(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(2)
        result = v1 + v2
        self.assertEqual(result.x, 5)

    def test_subtraction(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(1)
        result = v1 - v2
        self.assertEqual(result.x, 2)

    def test_equality(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(3)
        self.assertEqual(v1, v2)

    def test_inequality(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(4)
        self.assertNotEqual(v1, v2)

    def test_multiplication(self):
        v1 = Velocity1d(3)
        scalar = 2
        result = v1 * scalar
        self.assertEqual(result.x, 6)

    def test_from_meters_per_second(self):
        v = Velocity1d.from_meters_per_second(5)
        self.assertEqual(v.x, 5)

    def test_from_centimeters_per_second(self):
        v = Velocity1d.from_centimeters_per_second(500)
        self.assertEqual(v.x, 5)

    def test_from_inches_per_second(self):
        v = Velocity1d.from_inches_per_second(196.85)  # 5 meters
        self.assertAlmostEqual(v.x, 5, places=4)

    def test_from_feet_per_second(self):
        v = Velocity1d.from_feet_per_second(16.4042)  # 5 meters
        self.assertAlmostEqual(v.x, 5, places=4)

    def test_to_meters_per_second(self):
        v = Velocity1d(5)
        self.assertEqual(v.to_meters_per_second(), 5)

    def test_to_centimeters_per_second(self):
        v = Velocity1d(5)
        self.assertEqual(v.to_centimeters_per_second(), 500)

    def test_to_inches_per_second(self):
        v = Velocity1d(5)
        self.assertAlmostEqual(v.to_inches_per_second(), 196.85, places=2)

    def test_str(self):
        v = Velocity1d(5.0)
        self.assertEqual(str(v), "5.0 m/s")

    def test_speed_alias(self):
        v = Speed.from_meters_per_second(5)
        self.assertEqual(v.x, 5)


if __name__ == '__main__':
    unittest.main()
