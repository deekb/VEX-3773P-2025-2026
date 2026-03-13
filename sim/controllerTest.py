import evdev
from pyglet.input.linux.evdev_constants import ABS_RX

device = evdev.InputDevice('/dev/input/event19')

def process_raw_axis(value):
    return (value - 127) / 127



ABS_EVENT_CODE_MAP = {
    0: "LX",
    1: "LY",
    2: "RX",
    5: "RY"
}



latest_values = {}

for event in device.read_loop():
    # if event.type == evdev.ecodes.EV_KEY:
    #     print(evdev.categorize(event))
    if event.type == evdev.ecodes.EV_ABS:
        if event.code in EVENT_CODE_MAP:
            latest_values[EVENT_CODE_MAP[event.code]] = process_raw_axis(event.value)
    print([f"{key}:{value:.2f}" for key, value in latest_values.items()])

        # print(event)
