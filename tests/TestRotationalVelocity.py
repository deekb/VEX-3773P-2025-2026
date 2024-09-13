import unittest
from VEXLib.Geometry.RotationalVelocity import RotationalVelocity, RotSpeed

class TestRotationalVelocity(unittest.TestCase):
    def test_addition(self):
        v1 = RotationalVelocity.from_radians_per_second(3)
        v2 = RotationalVelocity.from_radians_per_second(2)
        result = v1 + v2
        self.assertEqual(result.velocity_radians_per_second, 5)

    def test_subtraction(self):
        v1 = RotationalVelocity.from_radians_per_second(3)
        v2 = RotationalVelocity.from_radians_per_second(1)
        result = v1 - v2
        self.assertEqual(result.velocity_radians_per_second, 2)

    def test_equality(self):
        v1 = RotationalVelocity.from_radians_per_second(3)
        v2 = RotationalVelocity.from_radians_per_second(3)
        self.assertEqual(v1, v2)

    def test_inequality(self):
        v1 = RotationalVelocity.from_radians_per_second(3)
        v2 = RotationalVelocity.from_radians_per_second(4)
        self.assertNotEqual(v1, v2)

    def test_multiplication(self):
        v1 = RotationalVelocity.from_radians_per_second(3)
        scalar = 2
        result = v1 * scalar
        self.assertEqual(result.velocity_radians_per_second, 6)

    def test_from_radians_per_second(self):
        v = RotationalVelocity.from_radians_per_second(5)
        self.assertEqual(v.velocity_radians_per_second, 5)

    def test_from_rotations_per_second(self):
        v = RotationalVelocity.from_rotations_per_second(0.7957747163688)
        self.assertAlmostEqual(v.velocity_radians_per_second, 5,  places=6)

    def test_from_rotations_per_minute(self):
        v = RotationalVelocity.from_rotations_per_minute(47.74648298)  # 5 rad/s
        self.assertAlmostEqual(v.velocity_radians_per_second, 5, places=6)

    def test_to_radians_per_second(self):
        v = RotationalVelocity.from_radians_per_second(5)
        self.assertEqual(v.to_radians_per_second(), 5)

    def test_to_rotations_per_second(self):
        v = RotationalVelocity.from_radians_per_second(5)
        self.assertAlmostEqual(v.to_rotations_per_second(), 0.7957747155, places=6)

    def test_to_rotations_per_minute(self):
        v = RotationalVelocity.from_radians_per_second(5)
        self.assertAlmostEqual(v.to_rotations_per_minute(), 47.74648298, places=6)

    def test_str(self):
        v = RotationalVelocity.from_radians_per_second(5.0)
        self.assertEqual(str(v), "5.0 rad/s")

    def test_rotSpeed_alias(self):
        v = RotSpeed.from_radians_per_second(5)
        self.assertEqual(v.velocity_radians_per_second, 5)


if __name__ == '__main__':
    unittest.main()
