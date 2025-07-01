class SplinePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SplineControlPoint(SplinePoint):
    def __init__(self, x, y):
        super().__init__(x, y)


class SplineSegment:
    def __init__(self, p0=None, p1=None, p2=None, p3=None):
        self.control_points = [p0, p1, p2, p3]

    @property
    def p0(self):
        return self.control_points[0]

    @p0.setter
    def p0(self, value):
        self.control_points[0] = value

    @property
    def p1(self):
        return self.control_points[1]

    @p1.setter
    def p1(self, value):
        self.control_points[1] = value

    @property
    def p2(self):
        return self.control_points[2]

    @p2.setter
    def p2(self, value):
        self.control_points[2] = value

    @property
    def p3(self):
        return self.control_points[3]

    @p3.setter
    def p3(self, value):
        self.control_points[3] = value

    def has_enough_points_to_discretize(self):
        return None not in self.control_points

    def discretize_segment(self, point_density=20):
        """Generates a Catmull-Rom spline segment between four control points."""
        curve = []

        # Generate spline points based on the Catmull-Rom formula
        for i in range(point_density):
            t = i / (point_density - 1)  # The T-value represents the percentage along the curve from 0 to 1
            t_squared = t * t
            t_cubed = t_squared * t
            a = [2 * self.p1.x, 2 * self.p1.y]
            b = [self.p2.x - self.p0.x, self.p2.y - self.p0.y]
            c = [
                2 * self.p0.x - 5 * self.p1.x + 4 * self.p2.x - self.p3.x,
                2 * self.p0.y - 5 * self.p1.y + 4 * self.p2.y - self.p3.y,
            ]
            d = [
                -self.p0.x + 3 * self.p1.x - 3 * self.p2.x + self.p3.x,
                -self.p0.y + 3 * self.p1.y - 3 * self.p2.y + self.p3.y,
            ]

            x = 0.5 * (a.x + b.x * t + c.x * t_squared + d.x * t_cubed)
            y = 0.5 * (a.y + b.y * t + c.y * t_squared + d.y * t_cubed)
            curve.append((x, y))

    # def link_to_previous(self, previous):
    #     self.linked_to =


# Abstract Spline class
class Spline:
    def __init__(self, point_density):
        self.segments: list[SplineSegment] = []
        self.point_density = point_density

    def generate(self):
        """Generate points for the spline based on control points."""
        raise NotImplementedError("Subclass must implement this method")


# Catmull-Rom Spline subclass
class CatmullRomSpline(Spline):
    def __init__(self, point_density=20):
        super().__init__(point_density)
        self.start_ghost = (0, 0)
        self.end_ghost = (0, 0)

    def discretize(self):
        if len(self.segments) < 1 or not self.segments.x.has_enough_points_to_discretize():
            return []

        # Smooth the start and end by creating 'ghost' points
        self.generate_ghost_points()
        print(f"Created ghost points at {self.start_ghost}, and {self.end_ghost}")
        # self.combine_segments()
        # extended_points = [self.start_ghost] + self.control_points + [self.end_ghost]
        #
        # # Generate the full spline by combining individual segments
        # full_spline = []
        # for i in range(1, len(extended_points) - 2):
        #     segment = self.segment(
        #         extended_points[i - 1],
        #         extended_points[i],
        #         extended_points[i + 1],
        #         extended_points[i + 2],
        #     )
        #     full_spline.extend(segment)

        # return full_spline

    def generate_ghost_points(self):
        first_segment = self.segments[0]
        last_segment = self.segments[-1]

        first_point, second_point = first_segment.p0, first_segment.p1
        last_point, second_last_point = last_segment.p3, last_segment.p2

        self.start_ghost = [
            2 * first_point.x - second_point.x,
            2 * first_point.y - second_point.y,
        ]  # Mirror the first point for smooth start

        self.end_ghost = [
            2 * last_point.x - second_last_point.x,
            2 * last_point.y - second_last_point.y,
        ]  # Mirror the last point for smooth end

    # def combine_segments(self):
    #     for segment in self.segments:
    #         segment = self.segment(
    #             extended_points[i - 1],
    #             extended_points[i],
    #             extended_points[i + 1],
    #             extended_points[i + 2],
    #         )
    #         full_spline.extend(segment)

    def add_segment(self, p0, p1, p2, p3):
        """Generates a Catmull-Rom spline segment between four control points."""
        self.segments.append(SplineSegment(SplineControlPoint(*p0), SplineControlPoint(*p1), SplineControlPoint(*p2), SplineControlPoint(*p3)))

        # curve = []
        #
        # # Generate spline points based on the Catmull-Rom formula
        # for i in range(self.point_density):
        #     t = i / (self.point_density - 1)
        #     t2, t3 = t * t, t * t * t
        #     a = [2 * p1[0], 2 * p1[1]]
        #     b = [p2[0] - p0[0], p2[1] - p0[1]]
        #     c = [
        #         2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0],
        #         2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1],
        #     ]
        #     d = [
        #         -p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0],
        #         -p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1],
        #     ]
        #
        #     x = 0.5 * (a[0] + b[0] * t + c[0] * t2 + d[0] * t3)
        #     y = 0.5 * (a[1] + b[1] * t + c[1] * t2 + d[1] * t3)
        #     curve.append((x, y))
        #
        # return curve

    def get_segments(self, index):
        return self.segments


spline = CatmullRomSpline()

print(f"Discretize with no segments: {spline.discretize()}")
spline.add_segment((0, 0), (0, 5), (5, 5), (5, 10))
print(f"Discretize with one segment: {spline.discretize()}")
