import math
import pygame


class NavigationEnvironment:
    def __init__(self, map_path):
        pygame.init()
        self.point_cloud_points = []
        self.map = pygame.image.load(map_path)
        self.display = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.display.blit(self.map, (0, 0))
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (128, 128, 128)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

    @staticmethod
    def angle_distance_to_cartesian(distance, angle, start_position):
        x = distance * math.cos(angle) + start_position[0]
        y = distance * math.sin(angle) + start_position[1]
        return int(x), int(y)

    def add_points_from_angle_distance(self, point_list):
        for point in point_list:
            point = self.angle_distance_to_cartesian(*point)
            if point not in self.point_cloud_points:
                self.point_cloud_points.append(point)

    def get_rendered_point_cloud(self, point_color=(255, 0, 0)):
        display_map = self.map.copy()
        display_map.fill((0, 0, 0))
        for point in self.point_cloud_points:
            display_map.set_at((point[0], point[1]), point_color)
        return display_map
