import unittest
from VEXLib.Geometry.Translation1d import Translation1d, Distance

class TestTranslation1d(unittest.TestCase):
    def test_addition(self):
        t1 = Translation1d(3)
        t2 = Translation1d(1)
        result = t1 + t2
        self.assertEqual(result.x, 4)

    def test_subtraction(self):
        t1 = Translation1d(3)
        t2 = Translation1d(1)
        result = t1 - t2
        self.assertEqual(result.x, 2)

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
        self.assertEqual(result.x, 6)

    def test_from_meters(self):
        t1 = Translation1d.from_meters(3)
        self.assertEqual(t1.x, 3)

    def test_from_centimeters(self):
        t1 = Translation1d.from_centimeters(300)
        self.assertAlmostEqual(t1.x, 3, places=6)

    def test_from_inches(self):
        t1 = Translation1d.from_inches(118.11)
        self.assertAlmostEqual(t1.x, 3, places=2)

    def test_from_feet(self):
        t1 = Translation1d.from_feet(9.84252)
        self.assertAlmostEqual(t1.x, 3, places=6)

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
        self.assertEqual(str(t1), "3.0 m")


if __name__ == '__main__':
    unittest.main()
