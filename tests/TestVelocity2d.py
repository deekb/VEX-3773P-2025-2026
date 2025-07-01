import unittest

from VEXLib.Geometry.Constants import VELOCITY2D_IDENTIFIER, SEPERATOR
from VEXLib.Geometry.Velocity2d import Velocity2d


class TestVelocity2d(unittest.TestCase):
    def test_addition(self):
        v1 = Velocity2d.from_meters_per_second(3, 4)
        v2 = Velocity2d.from_meters_per_second(1, 2)
        result = v1 + v2
        self.assertEqual(result.to_meters_per_second(), (4, 6))

    def test_subtraction(self):
        v1 = Velocity2d.from_meters_per_second(3, 4)
        v2 = Velocity2d.from_meters_per_second(1, 2)
        result = v1 - v2
        self.assertEqual(result.to_meters_per_second(), (2, 2))

    def test_equality(self):
        v1 = Velocity2d.from_meters_per_second(3, 4)
        v2 = Velocity2d.from_meters_per_second(3, 4)
        self.assertEqual(v1, v2)

    def test_inequality(self):
        v1 = Velocity2d.from_meters_per_second(3, 4)
        v2 = Velocity2d.from_meters_per_second(4, 5)
        self.assertNotEqual(v1, v2)

    def test_multiplication(self):
        v1 = Velocity2d.from_meters_per_second(3, 4)
        scalar = 2
        result = v1 * scalar
        self.assertEqual(result.to_meters_per_second(), (6, 8))

    def test_from_meters_per_second(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        self.assertEqual(v.to_meters_per_second(), (3, 4))

    def test_from_centimeters_per_second(self):
        v = Velocity2d.from_centimeters_per_second(300, 400)
        self.assertAlmostEqual(v.x_component.to_meters_per_second(), 3, places=4)
        self.assertAlmostEqual(v.y_component.to_meters_per_second(), 4, places=4)

    def test_from_inches_per_second(self):
        v = Velocity2d.from_inches_per_second(118.11, 157.48)
        self.assertAlmostEqual(v.x_component.to_meters_per_second(), 3, places=4)
        self.assertAlmostEqual(v.y_component.to_meters_per_second(), 4, places=4)

    def test_from_feet_per_second(self):
        v = Velocity2d.from_feet_per_second(9.84252, 13.1234)
        self.assertAlmostEqual(v.x_component.to_meters_per_second(), 3, places=4)
        self.assertAlmostEqual(v.y_component.to_meters_per_second(), 4, places=4)

    def test_to_meters_per_second(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        x, y = v.to_meters_per_second()
        self.assertEqual(x, 3)
        self.assertEqual(y, 4)

    def test_to_centimeters_per_second(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        self.assertEqual(v.to_centimeters_per_second(), (300, 400))

    def test_to_inches_per_second(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        x, y = v.to_inches_per_second()
        self.assertAlmostEqual(x, 118.11, places=2)
        self.assertAlmostEqual(y, 157.48, places=2)

    def test_angle_rad(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        self.assertAlmostEqual(v.angle_rad, 0.9273, places=4)

    def test_get_length(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        self.assertAlmostEqual(v.get_length().to_meters_per_second(), 5.0, places=3)

    def test_to_bytestring(self):
        v = Velocity2d.from_meters_per_second(3, 4)
        bytestring = v.to_bytestring()
        expected_bytestring = (
            VELOCITY2D_IDENTIFIER
            + b"0x1.8000000000000p+1"
            + SEPERATOR
            + b"0x1.0000000000000p+2"
        )
        self.assertEqual(bytestring, expected_bytestring)

    def test_from_bytestring(self):
        bytestring = (
            VELOCITY2D_IDENTIFIER
            + b"0x1.8000000000000p+1"
            + SEPERATOR
            + b"0x1.0000000000000p+2"
        )
        v = Velocity2d.from_bytestring(bytestring)
        self.assertEqual(v.to_meters_per_second(), (3, 4))


if __name__ == "__main__":
    unittest.main()
