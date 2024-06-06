import unittest
from VEXLib.Geometry.Translation2d import Translation2d


class TestTranslation2d(unittest.TestCase):
    def test_addition(self):
        t1 = Translation2d(3, 4)
        t2 = Translation2d(1, 2)
        result = t1 + t2
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)

    def test_subtraction(self):
        t1 = Translation2d(3, 4)
        t2 = Translation2d(1, 2)
        result = t1 - t2
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 2)

    def test_equality(self):
        t1 = Translation2d(3, 4)
        t2 = Translation2d(3, 4)
        self.assertEqual(t1, t2)

    def test_multiplication(self):
        t1 = Translation2d(3, 4)
        scalar = 2
        result = t1 * scalar
        self.assertEqual(result.x, 6)
        self.assertEqual(result.y, 8)


if __name__ == '__main__':
    unittest.main()
