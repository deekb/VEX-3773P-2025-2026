import vex
from VEXLib.Math import apply_deadband, cubic_filter
from VEXLib.Util import time
from VEXLib.Util.time import wait_until, wait_until_not


class DoublePressHandler:
    def __init__(self, pressed_callback, double_pressed_callback):
        self.last_press_time = time.time()
        self.double_press_time_threshold = 0.2
        self.pressed_callback = pressed_callback
        self.double_pressed_callback = double_pressed_callback

    def press(self):
        if time.time() - self.last_press_time < self.double_press_time_threshold:
            self.last_press_time = time.time()
            self.double_pressed_callback()
        else:
            self.last_press_time = time.time()
            self.pressed_callback()


class InputProcessor:
    def __init__(self):
        """
        Initialize the input processor with an empty pipeline.
        """
        self.pipeline = []

    def add_step(self, function):
        """
        Add a processing step to the pipeline.
        :param function: A callable function that takes input and returns processed output.
        """
        self.pipeline.append(function)

    def process(self, input_value):
        """
        Process the input through the pipeline.
        :param input_value: The initial input value to process.
        :return: The processed output.
        """
        for step in self.pipeline:
            input_value = step(input_value)
        return input_value


class Controller(vex.Controller):
    def __init__(self, controller_type=vex.ControllerType.PRIMARY):
        """
        Wrapper for the VEX Controller object.
        Args:
            controller_type: ControllerType.PRIMARY or ControllerType.PARTNER
        """
        self.controller = vex.Controller(controller_type)

        self.input_processor = InputProcessor()

    def add_deadband_step(self, deadband):
        self.input_processor.add_step(lambda x: apply_deadband(x, deadband, 1))

    def add_cubic_step(self, linearity):
        self.input_processor.add_step(lambda x: cubic_filter(x, linearity))

    def _get_axis_value_internal(self, axis):
        """
        Get the processed value of a controller axis.
        """
        return self.input_processor.process(axis.position() / 100)

    # ----- Joystick Methods -----
    def left_stick_x(self):
        """
        Get the X-axis value of the left stick (horizontal movement).
        """
        return self._get_axis_value_internal(self.controller.axis4)

    def left_stick_y(self):
        """
        Get the Y-axis value of the left stick (vertical movement).
        """
        return self._get_axis_value_internal(self.controller.axis3)

    def right_stick_x(self):
        """
        Get the X-axis value of the right stick (horizontal movement).
        """
        return self._get_axis_value_internal(self.controller.axis1)

    def right_stick_y(self):
        """
        Get the Y-axis value of the right stick (vertical movement).
        """
        return self._get_axis_value_internal(self.controller.axis2)

    def stick_values(self):
        """
        Get all stick values as a dictionary.
        :return: A dictionary with left and right stick X/Y values.
        """
        return {
            "left_stick_x": self.left_stick_x(),
            "left_stick_y": self.left_stick_y(),
            "right_stick_x": self.right_stick_x(),
            "right_stick_y": self.right_stick_y(),
        }

    def get_selection(self, options):
        """
        Allows the user to navigate through a list of options and select one using left/right and A.
        The function implements a loop to display and navigate through options on the controller.
        It reacts to button presses to modify the selection index or make a selection.

        Args:
            options (list): A list of options from which the user can select.

        Returns:
            selected (Any): The selected option from the list.
        """
        selection_index = 0

        wait_until_not(lambda: self.buttonA.pressing())

        while True:
            self.screen.clear_screen()
            self.screen.set_cursor(1, 1)
            self.screen.print(options[selection_index])
            wait_until(lambda: self.buttonRight.pressing() or self.buttonLeft.pressing() or self.buttonA.pressing())

            if self.buttonA.pressing():
                break

            if self.buttonRight.pressing():
                selection_index += 1
            elif self.buttonLeft.pressing():
                selection_index -= 1

            wait_until_not(lambda: self.buttonRight.pressing() or self.buttonLeft.pressing())

            if selection_index < 0:
                selection_index = 0
            elif selection_index >= len(options) - 1:
                selection_index = len(options) - 1
        wait_until_not(lambda: self.buttonA.pressing())

        return options[selection_index]
