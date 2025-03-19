import unittest
import math

from VEXLib.Algorithms.GravitationalFeedforward import GravitationalFeedforward


class TestGravitationalFeedforward(unittest.TestCase):
    def test_initialization(self):
        gf = GravitationalFeedforward(kg=1.0)
        self.assertEqual(gf.kg, 1.0)

    def test_update_horizontal(self):
        gf = GravitationalFeedforward(kg=1.0)
        output = gf.update(0.0)
        self.assertAlmostEqual(output, 0.0, places=5)

    def test_update_vertical(self):
        gf = GravitationalFeedforward(kg=1.0)
        output = gf.update(90.0)
        self.assertAlmostEqual(output, 1.0, places=5)

    def test_update_midway(self):
        gf = GravitationalFeedforward(kg=1.0)
        output = gf.update(45.0)
        self.assertAlmostEqual(output, math.sin(math.pi / 4), places=5)

    def test_update_wrap_around(self):
        gf = GravitationalFeedforward(kg=1.0)
        output = gf.update(270)
        self.assertAlmostEqual(output, -1.0, places=5)

    def test_update_with_gain(self):
        gf = GravitationalFeedforward(kg=2.0)
        output = gf.update(90)
        self.assertAlmostEqual(output, 2.0, places=5)


if __name__ == '__main__':
    unittest.main()