import os
import threading
from pyglet import image
from .windows import *


os.chdir(os.path.abspath(os.path.dirname(__name__)))
icon = image.load(WINDOW_ICON_NAME)

pyglet.resource.path = [RESOURCES_PATH]
pyglet.resource.reindex()

pyglet.font.add_file(FONT_NAME)
aller = pyglet.font.load(FONT_NAME, FONT_SIZE)


def main():
    robot_log_window = RobotLogWindow(500, 200, resizable=True)
    network_handler = NetworkHandler(HOST, PORT, robot_log_window)
    robot_actions_window = RobotActionsWindow(500, 500, network_handler)
    robot_status_window = RobotStatusWindow(500, 200, network_handler)

    robot_status_window.set_icon(icon)
    robot_actions_window.set_icon(icon)

    try:
        network_thread = threading.Thread(target=network_handler.start_network_loop)
        ping_rpi_thread = threading.Thread(target=network_handler.ping_rpi_loop)
        ping_robot_thread = threading.Thread(target=network_handler.ping_robot_loop)
        network_thread.start()
        ping_robot_thread.start()
        ping_rpi_thread.start()

        pyglet.app.run(1 / 30)
    except KeyboardInterrupt:
        pass
    print("Exiting")
    pyglet.app.exit()
    network_handler.shutdown()


if __name__ == "__main__":
    main()
