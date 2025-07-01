import unittest

from VEXLib.Geometry import GeometryUtil


class TestGeometryUtil(unittest.TestCase):

    def test_distance(self):
        self.assertAlmostEqual(GeometryUtil.distance((0, 0), (3, 4)), 5.0, places=5)
        self.assertAlmostEqual(GeometryUtil.distance((-1, -1), (2, 3)), 5.0, places=5)
        self.assertAlmostEqual(GeometryUtil.distance((0, 0), (0, 0)), 0.0, places=5)

    def test_area_triangle(self):
        self.assertAlmostEqual(
            GeometryUtil.area_triangle((0, 0), (3, 0), (3, 4)), 6.0, places=5
        )
        self.assertAlmostEqual(
            GeometryUtil.area_triangle((0, 0), (0, 3), (4, 3)), 6.0, places=5
        )
        self.assertAlmostEqual(
            GeometryUtil.area_triangle((0, 0), (0, 0), (0, 0)), 0.0, places=5
        )

    def test_centroid(self):

        self.assertAlmostEqual(
            GeometryUtil.centroid([(0.0, 0.0), (3.0, 0.0), (3.0, 4.0)]),
            (2.0, 4.0 / 3.0),
            places=5,
        )
        self.assertAlmostEqual(
            GeometryUtil.centroid([(0.0, 0.0), (0.0, 3.0), (4.0, 3.0)]),
            (4.0 / 3.0, 2.0),
            places=5,
        )

    def test_intersection_point(self):
        self.assertAlmostEqual(
            GeometryUtil.intersection_point((0, 0), (2, 2), (0, 2), (2, 0)),
            (1, 1),
            places=5,
        )
        self.assertIsNone(
            GeometryUtil.intersection_point((0, 0), (1, 1), (2, 2), (3, 3))
        )

    def test_is_point_inside_polygon(self):
        polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
        self.assertTrue(GeometryUtil.is_point_inside_polygon((2, 2), polygon))
        self.assertFalse(GeometryUtil.is_point_inside_polygon((5, 5), polygon))

    def test_polygon_area(self):
        polygon = [(0, 0), (3, 0), (3, 4), (0, 4)]
        self.assertAlmostEqual(GeometryUtil.polygon_area(polygon), 12.0, places=5)

    def test_circle_area(self):
        self.assertAlmostEqual(GeometryUtil.circle_area(5), 78.53981633974483, places=5)

    def test_circle_circumference(self):
        self.assertAlmostEqual(
            GeometryUtil.circle_circumference(5), 31.41592653589793, places=5
        )

    def test_rectangle_area(self):
        self.assertAlmostEqual(GeometryUtil.rectangle_area(3, 4), 12.0, places=5)

    def test_rectangle_perimeter(self):
        self.assertAlmostEqual(GeometryUtil.rectangle_perimeter(3, 4), 14.0, places=5)

    def test_closest_point_on_line(self):
        test_cases = [
            # point on line
            ((3, 4), (1, 1), (5, 5), (3.5, 3.5)),
            # point off line
            ((1, 2), (1, 1), (5, 5), (1.5, 1.5)),
            # vertical line
            ((2, 3), (2, 1), (2, 5), (2, 3)),
            # horizontal line
            ((2, 3), (1, 3), (5, 3), (2, 3)),
            # point equals line start
            ((1, 1), (1, 1), (5, 5), (1, 1)),
            # point equals line end
            ((5, 5), (1, 1), (5, 5), (5, 5)),
        ]

        for point, line_start, line_end, expected_closest_point in test_cases:
            with self.subTest(point=point, line_start=line_start, line_end=line_end):
                closest_point = GeometryUtil.closest_point_on_line(
                    point, line_start, line_end
                )
                self.assertEqual(closest_point, expected_closest_point)


if __name__ == "__main__":
    unittest.main()
