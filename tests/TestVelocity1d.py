import unittest
from VEXLib.Geometry.Velocity1d import Velocity1d, Speed
from VEXLib.Geometry.Constants import VELOCITY1D_IDENTIFIER


class TestVelocity1d(unittest.TestCase):
    def test_addition(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(2)
        result = v1 + v2
        self.assertEqual(result.magnitude, 5)

    def test_subtraction(self):
        v1 = Velocity1d(3)
        v2 = Velocity1d(1)
        result = v1 - v2
        self.assertEqual(result.magnitude, 2)

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
        self.assertEqual(result.magnitude, 6)

    def test_from_meters_per_second(self):
        v = Velocity1d.from_meters_per_second(5)
        self.assertEqual(v.magnitude, 5)

    def test_from_centimeters_per_second(self):
        v = Velocity1d.from_centimeters_per_second(500)
        self.assertEqual(v.magnitude, 5)

    def test_from_inches_per_second(self):
        v = Velocity1d.from_inches_per_second(196.85)  # 5 meters
        self.assertAlmostEqual(v.magnitude, 5, places=4)

    def test_from_feet_per_second(self):
        v = Velocity1d.from_feet_per_second(16.4042)  # 5 meters
        self.assertAlmostEqual(v.magnitude, 5, places=4)

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
        self.assertEqual(f"Velocity1d<{v.to_meters_per_second()} m/s>", str(v))

    def test_speed_alias(self):
        v = Speed.from_meters_per_second(5)
        self.assertEqual(v.magnitude, 5)

    def test_to_bytestring(self):
        v = Velocity1d(5)
        bytestring = v.to_bytestring()
        expected_bytestring = VELOCITY1D_IDENTIFIER + b'0x1.4000000000000p+2'
        self.assertEqual(bytestring, expected_bytestring)

    def test_from_bytestring(self):
        bytestring = VELOCITY1D_IDENTIFIER + b'0x1.4000000000000p+2'
        v = Velocity1d.from_bytestring(bytestring)
        self.assertEqual(v.magnitude, 5)


if __name__ == '__main__':
    unittest.main()
