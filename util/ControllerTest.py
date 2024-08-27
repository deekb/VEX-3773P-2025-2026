import pyglet

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Joystick Positions")

# Load joysticks
joysticks = pyglet.input.get_joysticks()
if joysticks:
    joysticks[0].open()


@window.event
def on_draw():
    window.clear()

    if joysticks:
        joystick = joysticks[0]

        # print(help(joystick.rx_control))

        # Get joystick positions
        x1, y1 = joystick.rz, joystick.y
        x2, y2 = joystick.rx, joystick.ry
        print(x1, y1)
        print(x2, y2)

        # Scale positions to window size
        x1_pos = 400 + x1 * 200
        y1_pos = 300 + y1 * 200
        x2_pos = 400 + x2 * 200
        y2_pos = 300 + y2 * 200

        # Draw circles at joystick positions
        pyglet.shapes.Circle(x1_pos, y1_pos, 10, color=(255, 0, 0, 128)).draw()
        pyglet.shapes.Circle(x2_pos, y2_pos, 10, color=(0, 255, 0, 128)).draw()


# Run the application
pyglet.app.run()
