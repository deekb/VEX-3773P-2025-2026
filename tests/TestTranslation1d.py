import unittest
from VEXLib.Geometry.Translation1d import Translation1d, Distance
from VEXLib.Geometry.Constants import TRANSLATION1D_IDENTIFIER


class TestTranslation1d(unittest.TestCase):
    def test_addition(self):
        t1 = Translation1d(3)
        t2 = Translation1d(1)
        result = t1 + t2
        self.assertEqual(result.magnitude, 4)

    def test_subtraction(self):
        t1 = Translation1d(3)
        t2 = Translation1d(1)
        result = t1 - t2
        self.assertEqual(result.magnitude, 2)

    def test_equality(self):
        t1 = Translation1d(3)
        t2 = Translation1d(3)
        self.assertEqual(t1, t2)

    def test_inequality(self):
        t1 = Translation1d(3)
        t2 = Translation1d(4)
        self.assertNotEqual(t1, t2)

    def test_multiplication(self):
        t1 = Translation1d(3)
        scalar = 2
        result = t1 * scalar
        self.assertEqual(result.magnitude, 6)

    def test_from_meters(self):
        t1 = Translation1d.from_meters(3)
        self.assertEqual(t1.magnitude, 3)

    def test_from_centimeters(self):
        t1 = Translation1d.from_centimeters(300)
        self.assertAlmostEqual(t1.magnitude, 3, places=6)

    def test_from_inches(self):
        t1 = Translation1d.from_inches(118.11)
        self.assertAlmostEqual(t1.magnitude, 3, places=2)

    def test_from_feet(self):
        t1 = Translation1d.from_feet(9.84252)
        self.assertAlmostEqual(t1.magnitude, 3, places=6)

    def test_to_meters(self):
        t1 = Translation1d(3)
        self.assertEqual(t1.to_meters(), 3)

    def test_to_centimeters(self):
        t1 = Translation1d(3)
        self.assertEqual(t1.to_centimeters(), 300)

    def test_to_inches(self):
        t1 = Translation1d(3)
        self.assertAlmostEqual(t1.to_inches(), 118.11, places=2)

    def test_to_feet(self):
        t1 = Translation1d(3)
        self.assertAlmostEqual(t1.to_feet(), 9.84252, places=5)

    def test_distance_alias(self):
        t1 = Distance.from_meters(1)
        self.assertEqual(t1.to_meters(), 1)

    def test_str(self):
        t1 = Translation1d(3.0)
        self.assertEqual(str(t1), "3.0m")

    def test_inverse(self):
        t1 = Translation1d(3)
        result = t1.inverse()
        self.assertEqual(result.magnitude, -3)

    def test_to_bytestring(self):
        t1 = Translation1d(3)
        bytestring = t1.to_bytestring()
        expected_bytestring = TRANSLATION1D_IDENTIFIER + b'0x1.8000000000000p+1'
        self.assertEqual(bytestring, expected_bytestring)

    def test_from_bytestring(self):
        bytestring = TRANSLATION1D_IDENTIFIER + b'0x1.8000000000000p+1'
        t1 = Translation1d.from_bytestring(bytestring)
        self.assertEqual(t1.magnitude, 3)


if __name__ == '__main__':
    unittest.main()