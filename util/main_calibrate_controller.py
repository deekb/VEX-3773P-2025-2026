from VEXLib.Util.Logging import Logger

import VEXLib.Util.time as time
from VEXLib.Geometry.GeometryUtil import hypotenuse
from VEXLib.Sensors.Controller import Controller
from VEXLib.Util.Logging import TimeSeriesLogger
from vex import Brain


def main(brain: Brain, _):
    main_log = Logger("logs/joystick_calibrations")
    controller = Controller()
    left_stick_logger = TimeSeriesLogger("left_stick", ["x", "y"])
    right_stick_logger = TimeSeriesLogger("right_stick", ["x", "y"])

    brain.screen.print("Move the left stick all the way up and press A")
    brain.screen.next_row()
    time.wait_until(controller.buttonA.pressing)
    time.wait_until_not(controller.buttonA.pressing)
    brain.screen.print("Calibrating left stick")
    brain.screen.next_row()
    brain.screen.print("Now roll the joystick around in")
    brain.screen.next_row()
    brain.screen.print("a circle at least 3 times, taking")
    brain.screen.next_row()
    brain.screen.print("around one 2 seconds per revolution")
    brain.screen.next_row()

    main_log.info("Starting left joystick calibration")
    start_time = time.time()
    while time.time() - start_time < 6:
        x, y = controller.left_stick_position_raw()
        if hypotenuse(x, y) > 0.8:
            left_stick_logger.write_data({"x": x, "y": y})
    brain.screen.print("Done")
    time.sleep(2)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    brain.screen.print("Move the right stick all the way up and press A")
    brain.screen.next_row()
    time.wait_until(controller.buttonA.pressing)
    time.wait_until_not(controller.buttonA.pressing)
    brain.screen.print("Calibrating right stick")
    brain.screen.next_row()
    main_log.info("Starting right joystick calibration")
    start_time = time.time()
    while time.time() - start_time < 6:
        x, y = controller.right_stick_position_raw()
        if hypotenuse(x, y) > 0.8:
            right_stick_logger.write_data({"x": x, "y": y})
