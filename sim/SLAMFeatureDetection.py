import numpy as np
import math
from fractions import Fraction


class FeatureDetection:
    def __init__(self):
        self.epsilon = 10
        self.delta = 501
        self.snum = 6
        self.pmin = 20
        self.gmax = 20
        self.seed_segments = []
        self.line_segments = []
        self.laser_points = []
        self.line_params = None
        self.np = len(self.laser_points) - 1
        self.lmin = 20  # Minimum line segment length
        self.lr = 0  # The real length of a line segment
        self.pr = 0  # The number of points contained in the line segment

    def distance(self, point1, point2):
        return math.dist(point1, point2)

    # def disttance_point_to_line(self, ):
