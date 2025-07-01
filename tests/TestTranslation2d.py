import unittest

from VEXLib.Geometry.Constants import TRANSLATION2D_IDENTIFIER, SEPERATOR
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation2d import Translation2d


class TestTranslation2d(unittest.TestCase):
    def test_addition(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(1, 2)
        result = t1 + t2
        self.assertEqual(result.to_meters(), (4, 6))

    def test_subtraction(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(1, 2)
        result = t1 - t2
        self.assertEqual(result.to_meters(), (2, 2))

    def test_equality(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(3, 4)
        self.assertEqual(t1, t2)

    def test_multiplication(self):
        t1 = Translation2d.from_meters(3, 4)
        scalar = 2
        result = t1 * scalar
        self.assertEqual(result.to_meters(), (6, 8))

    def test_from_meters(self):
        t = Translation2d.from_meters(3, 4)
        self.assertEqual(t.to_meters(), (3, 4))

    def test_from_centimeters(self):
        t = Translation2d.from_centimeters(300, 400)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_from_inches(self):
        t = Translation2d.from_inches(118.11, 157.48)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_from_feet(self):
        t = Translation2d.from_feet(9.84252, 13.1234)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_to_meters(self):
        t = Translation2d.from_meters(3, 4)
        x, y = t.to_meters()
        self.assertEqual(x, 3)
        self.assertEqual(y, 4)

    def test_to_centimeters(self):
        t = Translation2d.from_meters(3, 4)
        self.assertEqual(t.to_centimeters(), (300, 400))

    def test_to_inches(self):
        t = Translation2d.from_meters(3, 4)
        x, y = t.to_inches()
        self.assertAlmostEqual(x, 118.11, places=2)
        self.assertAlmostEqual(y, 157.48, places=2)

    def test_distance(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(1, 2)
        self.assertAlmostEqual(t1.distance(t2).to_meters(), 2.828, places=3)

    def test_length(self):
        t = Translation2d.from_meters(3, 4)
        self.assertAlmostEqual(t.length().to_meters(), 5.0, places=3)

    def test_rotate_by(self):
        t = Translation2d.from_meters(1, 0)
        rotation = Rotation2d.from_degrees(90)
        rotated = t.rotate_by(rotation)
        self.assertAlmostEqual(rotated.to_meters()[0], 0.0, places=3)
        self.assertAlmostEqual(rotated.to_meters()[1], 1.0, places=3)

    def test_inverse(self):
        t = Translation2d.from_meters(3, 4)
        result = t.inverse()
        self.assertAlmostEqual(result.to_meters()[0], -3, places=3)
        self.assertAlmostEqual(result.to_meters()[1], -4, places=3)

    def test_to_bytestring(self):
        t = Translation2d.from_meters(3, 4)
        bytestring = t.to_bytestring()
        expected_bytestring = (
            TRANSLATION2D_IDENTIFIER
            + b"0x1.8000000000000p+1"
            + SEPERATOR
            + b"0x1.0000000000000p+2"
        )
        self.assertEqual(bytestring, expected_bytestring)

    def test_from_bytestring(self):
        bytestring = (
            TRANSLATION2D_IDENTIFIER
            + b"0x1.8000000000000p+1"
            + SEPERATOR
            + b"0x1.0000000000000p+2"
        )
        t = Translation2d.from_bytestring(bytestring)
        self.assertEqual(t.to_meters(), (3, 4))


if __name__ == "__main__":
    unittest.main()
