import numpy as np
import pygame
import math


def add_uncertainty(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma ** 2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(0, distance)
    angle = max(0, angle)
    return [distance, angle]


def interpolate(x1: float, x2: float, y1: float, y2: float, fraction: float) -> tuple:
    """
    Perform linear interpolation for x between (x1, y1) and (x2, y2)

    Args:
        x1 (float): The X value of the first point.
        x2 (float): The X value of the second point.
        y1 (float): The Y value of the first point.
        y2 (float): The Y value of the second point.
        fraction (float): The fraction between the points (x1, y1) and (x2, y2) to interpolate the coordinates for.

    Returns:
        tuple: A tuple containing the interpolated X and Y values between (x1, y1) and (x2, y2).
    """
    # Perform linear interpolation for both x and y
    interpolated_x = x1 + (fraction * (x2 - x1))
    interpolated_y = y1 + (fraction * (y2 - y1))

    return interpolated_x, interpolated_y


class LaserSensor:
    def __init__(self, max_range, map, uncertainty, pygame_display, speed=4):
        self.max_range = max_range
        self.speed = speed
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0, 0)
        self.pygame_display = pygame_display
        self.map = map
        self.width, self.height = pygame.display.get_surface().get_size()
        self.sensed_obstacles = []

    def distance_to_obstacle(self, obstacle_position):
        return math.hypot(obstacle_position[0] - self.position[0], obstacle_position[1] - self.position[1])

    def sense_obstacles(self, rotations_rad=2 * math.pi, rotation_steps=256, pixel_sample_steps=100):
        collision_points = []
        current_x, current_y = self.position
        for angle in np.linspace(0, rotations_rad, rotation_steps):
            endpoint_x, endpoint_y = self.max_range * math.cos(angle) + current_x, self.max_range * math.sin(
                angle) + current_y
            for distance in np.linspace(0, self.max_range, pixel_sample_steps):
                fraction_complete = distance / self.max_range
                test_x, test_y = interpolate(current_x, endpoint_x, current_y, endpoint_y, fraction_complete)
                if 0 < test_x < self.width and 0 < test_y < self.height:
                    # Ensure that the pixel is inside the window
                    color = self.map.get_at((int(test_x), int(test_y)))
                    if color == (0, 0, 0):
                        distance = self.distance_to_obstacle((test_x, test_y))
                        distance_with_uncertainty = add_uncertainty(distance, angle, self.sigma)
                        distance_with_uncertainty.append(self.position)
                        collision_points.append(distance_with_uncertainty)
                        break
        if not collision_points:
            return None
        return collision_points
