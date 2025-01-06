from abc import ABC

import pyglet
from .config import *
from .network_handler import NetworkHandler
from pyglet.gui import PushButton


class RobotStatusWindow(pyglet.window.Window):
    def __init__(self, width, height, network_handler: NetworkHandler, **kwargs):
        super().__init__(width, height, "Robot Status", **kwargs)
        self.network_handler = network_handler

        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)

        self.rpi_online_image = pyglet.sprite.Sprite(pyglet.resource.image("access-point-1.png"), x=0, y=64)
        self.rpi_offline_image = pyglet.sprite.Sprite(pyglet.resource.image("access-point-off-1.png"), x=0, y=64)

        self.robot_online_image = pyglet.sprite.Sprite(pyglet.resource.image("robot-outline-1.png"), x=0, y=0)
        self.robot_offline_image = pyglet.sprite.Sprite(pyglet.resource.image("robot-off-outline-1.png"), x=0, y=0)

        self.rpi_status_label = pyglet.text.Label("Offline", x=64, y=64, font_size=40, anchor_x='left',
                                                  anchor_y='bottom', color=(255, 0, 0, 255), font_name=FONT_NAME, )

        self.robot_status_label = pyglet.text.Label("Offline", x=64, y=0, font_size=40, anchor_x='left',
                                                    anchor_y='bottom', color=(255, 0, 0, 255), font_name=FONT_NAME, )

        self.ping_time_label = pyglet.text.Label(f"Offline", font_size=20, x=self.width, y=self.height,
                                                 anchor_x='right', anchor_y='top', color=(255, 0, 0, 255),
                                                 font_name=FONT_NAME, )

    def draw_robot_status(self, online):
        if online:
            self.robot_status_label.text = "Online"
            self.robot_status_label.color = (0, 255, 0, 255)
            self.robot_online_image.draw()
        else:
            self.robot_status_label.text = "Offline"
            self.robot_status_label.color = (255, 0, 0, 255)
            self.robot_offline_image.draw()

    def draw_rpi_status(self, online):
        if online:
            self.rpi_status_label.text = "Online"
            self.rpi_status_label.color = (0, 255, 0, 255)
            self.rpi_online_image.draw()
        else:
            self.rpi_status_label.text = "Offline"
            self.rpi_status_label.color = (255, 0, 0, 255)
            self.rpi_offline_image.draw()

    def draw_ping_status(self, online):
        if online:
            self.ping_time_label.text = f"Ping: {round(self.network_handler.robot_ping_time())}ms"
            self.ping_time_label.color = (0, 255, 0, 255) if self.network_handler.robot_ping_time() <= 100 else (
                255, 0, 0, 255)
        else:
            self.ping_time_label.text = "Ping: Offline"
            self.ping_time_label.color = (255, 0, 0, 255)

    def draw_status(self):

        rpi_online = self.network_handler.communications_online()
        robot_online = self.network_handler.robot_is_online() and rpi_online  # Robot can't be online unless rpi is

        self.draw_ping_status(robot_online)
        self.draw_robot_status(robot_online)
        self.draw_rpi_status(rpi_online)

        self.ping_time_label.draw()
        self.robot_status_label.draw()
        self.rpi_status_label.draw()

    def on_draw(self):
        self.clear()
        self.background_image.blit(0, 0)
        self.draw_status()

    def on_resize(self, *args):
        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)


class RobotLogWindow(pyglet.window.Window):
    def __init__(self, width, height, **kwargs):
        super().__init__(width, height, "VexLog", **kwargs)

        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)

        self.text = ""
        self.log_label = pyglet.text.Label(self.text, font_size=16, anchor_x='left', anchor_y='top',
                                           color=(0, 255, 0, 255), multiline=True, width=width, font_name=FONT_NAME, )

    def on_draw(self):
        self.clear()
        self.background_image.blit(0, 0)
        last_20 = self.text.split("\n")[-20:]

        self.log_label = pyglet.text.Label("\n".join(last_20), x=0, y=self.height, font_size=16, anchor_x='left',
                                           anchor_y='top', color=(255, 255, 255, 255), multiline=True, width=self.width,
                                           font_name=FONT_NAME, )
        self.log_label.draw()

    def on_resize(self, *args):
        print("on_resize fired")
        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)

    def log(self, text, end="\n"):
        self.text += str(text) + str(end)


class RobotActionsWindow(pyglet.window.Window):
    def __init__(self, width, height, network_handler: NetworkHandler, **kwargs):
        super().__init__(width, height, "Robot Actions", **kwargs)
        self.network_handler = network_handler

        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)

        restart_image = pyglet.resource.image("restart-1.png")
        power_cycle_image = pyglet.resource.image("power-cycle-1.png")

        self.restart_robot_button = PushButton(0, self.height - 64, restart_image, restart_image)
        self.restart_bridge_button = PushButton(0, self.height - 128, restart_image, restart_image)
        self.restart_rpi_button = PushButton(0, self.height - 192, power_cycle_image, power_cycle_image)

        self.restart_robot_label = pyglet.text.Label("Restart robot", x=64, y=self.height, font_size=40,
                                                     anchor_x='left', anchor_y='top', color=(255, 255, 255, 255),
                                                     font_name=FONT_NAME, )

        self.restart_bridge_label = pyglet.text.Label("Restart bridge", x=64, y=self.height - 64, font_size=40,
                                                      anchor_x='left', anchor_y='top', color=(255, 255, 255, 255),
                                                      font_name=FONT_NAME, )

        self.restart_rpi_label = pyglet.text.Label("Restart RPI", x=64, y=self.height - 128, font_size=40,
                                                   anchor_x='left', anchor_y='top', color=(255, 255, 255, 255),
                                                   font_name=FONT_NAME, )

        self.push_handlers(self.restart_robot_button)
        self.push_handlers(self.restart_bridge_button)
        self.push_handlers(self.restart_rpi_button)

        self.restart_robot_button.set_handler('on_press', self.network_handler.restart_robot)
        self.restart_bridge_button.set_handler('on_press', self.network_handler.restart_rpi_bridge)
        self.restart_rpi_button.set_handler('on_press',
                                            self.network_handler.restart_rpi)  # self.button.set_handler('on_release', my_on_release_handler)

    def on_draw(self, *args):
        self.clear()
        self.background_image.blit(0, 0)
        for sprite in [self.restart_robot_button._sprite, self.restart_bridge_button._sprite,
                       self.restart_rpi_button._sprite, self.restart_robot_label, self.restart_bridge_label,
                       self.restart_rpi_label]:
            sprite.draw()

    def on_resize(self, *args):
        self.background_image = pyglet.image.SolidColorImagePattern((30, 43, 54, 255)).create_image(self.width,
                                                                                                    self.height)
