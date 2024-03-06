import threading

import pyglet
import socket


# Socket parameters
HOST = "vex-rpi.local"
PORT = 10001  # Port to connect to (non-privileged ports are >= 1024)

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((HOST, PORT))


class VexBoard:
    def __init__(self):
        self.widgets = {}

    def add_widget(self, name, initial_value):
        self.widgets[name] = VexBoardWidget(name, initial_value)

    def update_widget(self, name, new_value):
        if name in self.widgets:
            self.widgets[name].update_value(new_value)
        else:
            print(f"Widget \"{name}\" does not exist.")


class VexBoardWidget:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def update_value(self, new_value):
        self.value = new_value


class VexBoardWindow(pyglet.window.Window):
    def __init__(self, width, height, shuffleboard):
        super().__init__(width, height, "VexBoard")
        self.vex_board = shuffleboard
        self.labels = []

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            my_socket.sendall("LMB:{}|{}\n".format(x, y).encode())
        elif button == pyglet.window.mouse.RIGHT:
            my_socket.sendall("RMB:{}|{}\n".format(x, y).encode())
        elif button == pyglet.window.mouse.MIDDLE:
            my_socket.sendall("MMB:{}|{}\n".format(x, y).encode())

    def update_labels(self):
        for label in self.labels:
            label.delete()
        self.labels = []

        for i, widget in enumerate(self.vex_board.widgets.values()):
            label = pyglet.text.Label(f"{widget.name}: {widget.value}",
                                      font_size=16,
                                      x=10,
                                      y=self.height - (i + 1) * 30,
                                      anchor_x='left',
                                      anchor_y='top')
            self.labels.append(label)

    def on_draw(self):
        self.clear()
        self.update_labels()
        for label in self.labels:
            label.draw()


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return "%d:%02d:%02d" % (hours, minutes, seconds)


def network_loop():
    my_socket.recv(4096)
    while True:
        received = my_socket.recv(1024).strip(b"\n")
        if b"time:" in received:
            try:
                vex_board.update_widget("Uptime", format_time(float(received[5:])))
            except ValueError:
                pass


# Example usage:
if __name__ == "__main__":
    network_thread = threading.Thread(target=network_loop)
    network_thread.start()

    vex_board = VexBoard()
    vex_board.add_widget("Speed", 0)
    vex_board.add_widget("Temperature", 25)
    vex_board.add_widget("Voltage", 12.5)
    vex_board.add_widget("Uptime", 0)

    window = VexBoardWindow(600, 600, vex_board)
    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        pyglet.app.exit()
