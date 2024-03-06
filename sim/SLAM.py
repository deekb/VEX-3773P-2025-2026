import os

import SLAMSensors
from SLAMNagigationEnvironment import NavigationEnvironment
import math
import pygame


base_directory = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(base_directory, 'resources')


environment = NavigationEnvironment(os.path.join(resource_path, "SLAMMap.png"))
laser_sensor = SLAMSensors.LaserSensor(100, environment.map, (0.5, 0.01), environment.display)

running = True
sensor_active = False
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sensor_active = pygame.mouse.get_focused()

    if sensor_active:
        mouse_position = pygame.mouse.get_pos()
        laser_sensor.position = mouse_position
        sensor_data = laser_sensor.sense_obstacles()
        if sensor_data:
            environment.add_points_from_angle_distance(sensor_data)
        rendered = environment.get_rendered_point_cloud()
        environment.display.blit(rendered, (0, 0))

    print(clock.get_fps())

    pygame.display.flip()
    clock.tick(60)
