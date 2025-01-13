import vex
from VEXLib.Math import apply_deadband


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
    def __init__(self, controllerType=vex.ControllerType.PRIMARY):
        """
        Wrapper for the VEX Controller object.
        :param controllerType: ControllerType.PRIMARY or ControllerType.PARTNER
        """
        self.controller = vex.Controller(controllerType)
        self.deadband = 0.0

    def _get_axis_value_internal(self, axis):
        """
        Get the deadbanded value of a controller axis.
        """
        return apply_deadband(axis.position() / 100, self.deadband, 1)

    # ----- Stick (Joystick) Methods -----
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
