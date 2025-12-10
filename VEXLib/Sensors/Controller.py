import vex
from VEXLib.Kinematics import desaturate_wheel_speeds
from VEXLib.Math import apply_deadband, cubic_filter, MathUtil
from VEXLib.Util import time
from VEXLib.Util.time import wait_until, wait_until_not
import collections

class ControlStyles:
    TANK = 1
    ARCADE = 2
    SPLIT_ARCADE = 3


class DoublePressHandler:
    def __init__(
        self,
        pressed_callback,
        double_pressed_callback,
        timeout_threshold=0.2,
        delayed_call=False,
    ):
        """
        This class allows you to map one action to a button and another action to the second time the button is pressed within timeout_threshold seconds
        We used this during the 2024-2025 High Stakes season in order to have a button that moved the wall-stake mechanism in by one state, and also
        have a way to quickly skip the middle state of the wall stake when it was pressed twice in quick succession.

        PLEASE NOTE: the pressed_callback will be called every time you press the button, unless it was pressed within the last timeout_threshold seconds,
        doing it this way prevents unnecessary input delay

        Coming soon:
            if you would like the code to instead delay timeout_threshold seconds before calling any function you can set the flag delayed_call to True

        Args:
            pressed_callback:
            double_pressed_callback:
        """
        # TODO: Implement delayed_call
        self.last_press_time = time.time()
        self.timeout_threshold = timeout_threshold
        self.pressed_callback = pressed_callback
        self.double_pressed_callback = double_pressed_callback

    def press(self):
        if time.time() - self.last_press_time < self.timeout_threshold:
            self.last_press_time = time.time()
            self.double_pressed_callback()
        else:
            self.last_press_time = time.time()
            self.pressed_callback()


class InputProcessor:
    def __init__(self):
        """
        Initialize the input processor with an empty pipeline.
        The input processor is a pipeline, meaning a structure that allows applying generic steps to an input in order to produce an output
        In this case the InputProcessor is used to take input from the controller (along one axis from -1 to 1) and apply functions like deadzoning, tunable cubic filtering, and
        """
        self.pipeline = []

    def add_step(self, function):
        """
        Add a processing step to the pipeline.
        Args:
             function: A callable function that takes input and returns processed output.
        """
        self.pipeline.append(function)

    def process(self, input_value):
        """
        Process the input through the pipeline.
        Args:
            input_value: The initial input value to process.
        Returns
            output (Any): The processed output.
        """
        for step in self.pipeline:
            input_value = step(input_value)
        return input_value


class Controller(vex.Controller):
    def __init__(self, controller_type=vex.ControllerType.PRIMARY):
        """
        Wrapper for the VEX Controller object. Adds left_stick_x, left_stick_y, right_stick_x, right_stick_y functions
        that return outputs in range -1 to 1, uses an input processor internally to allow for adding modular steps
        such as deadzoning or cubic filtering, see InputProcessor for more details
        Args:
            controller_type: ControllerType.PRIMARY or ControllerType.PARTNER
        """
        super().__init__(controller_type)

        self.input_processor = InputProcessor()

    def add_deadband_step(self, deadband):
        self.input_processor.add_step(lambda x: apply_deadband(x, deadband, 1))

    def add_cubic_step(self, linearity=0.5):
        """Adds a cubic filter step to the input processor pipeline, I recommend doing this after any deadzoning you do

        Args:
            linearity: The linearity argument allows you to linearly interpolate between a pure cubic curve (y = x ** 3) and a pure linear function (y = x), this changes how aggressively the cubic function is applied.
        """
        self.input_processor.add_step(lambda x: cubic_filter(x, linearity))

    @staticmethod
    def _get_raw_axis_value(axis):
        """
        Get the processed value of a controller axis.

        Args:
            axis: The controller axis object to get the raw value of

        Returns:
            value (float): The raw value from -1 to +1 of the supplied axis object
        """
        return axis.position() / 100.0

    def _get_processed_axis_value(self, axis):
        """
        Get the processed value of a controller axis.

        Args:
            axis (vex.): The axis
        """
        return self.input_processor.process(self._get_raw_axis_value(axis))

    # ----- Joystick Methods -----
    def left_stick_x(self):
        """
        Get the PROCESSED X-axis value of the left stick (horizontal movement, range -1 to +1 unless one of your InputProcessor steps scales it to a different range).
        """
        return self._get_processed_axis_value(self.axis4)

    def left_stick_x_raw(self):
        """
        Get the RAW X-axis value of the left stick (horizontal movement, range -1 to +1).
        """
        return self._get_raw_axis_value(self.axis4)

    def left_stick_y(self):
        """
        Get the PROCESSED Y-axis value of the left stick (vertical movement, range -1 to +1 unless one of your InputProcessor steps scales it to a different range).
        """
        return self._get_processed_axis_value(self.axis3)

    def left_stick_y_raw(self):
        """
        Get the RAW Y-axis value of the left stick (vertical movement, range -1 to +1).
        """
        return self._get_raw_axis_value(self.axis3)

    def right_stick_x(self):
        """
        Get the PROCESSED X-axis value of the right stick (horizontal movement, range -1 to +1 unless one of your InputProcessor steps scales it to a different range).
        """
        return self._get_processed_axis_value(self.axis1)

    def right_stick_x_raw(self):
        """
        Get the RAW X-axis value of the right stick (horizontal movement, range -1 to +1).
        """
        return self._get_raw_axis_value(self.axis1)

    def right_stick_y(self):
        """
        Get the PROCESSED Y-axis value of the right stick (vertical movement, range -1 to +1 unless one of your InputProcessor steps scales it to a different range).
        """
        return self._get_processed_axis_value(self.axis2)

    def right_stick_y_raw(self):
        """
        Get the RAW Y-axis value of the right stick (vertical movement, range -1 to +1.
        """
        return self._get_raw_axis_value(self.axis2)

    def left_stick_position(self):
        """
        Get the PROCESSED position of the left stick as a tuple (x, y).

        Returns:
            tuple: A tuple containing the processed X and Y values of the left stick.
        """
        return self.left_stick_x(), self.left_stick_y()

    def left_stick_position_raw(self):
        """
        Get the RAW position of the left stick as a tuple (x, y).

        Returns:
            tuple: A tuple containing the raw X and Y values of the left stick.
        """
        return self.left_stick_x_raw(), self.left_stick_y_raw()

    def right_stick_position(self):
        """
        Get the PROCESSED position of the right stick as a tuple (x, y).

        Returns:
            tuple: A tuple containing the processed X and Y values of the right stick.
        """
        return self.right_stick_x(), self.right_stick_y()

    def right_stick_position_raw(self):
        """
        Get the RAW position of the right stick as a tuple (x, y).

        Returns:
            tuple: A tuple containing the raw X and Y values of the right stick.
        """
        return self.right_stick_x_raw(), self.right_stick_y_raw()

    def stick_values(self):
        """
        Get all PROCESSED stick values as a dictionary.

        Returns:
            processed_values: A dictionary with processed left and right stick X/Y values.
        """
        return {
            "left_stick_x": self.left_stick_x(),
            "left_stick_y": self.left_stick_y(),
            "right_stick_x": self.right_stick_x(),
            "right_stick_y": self.right_stick_y(),
        }

    def stick_values_raw(self):
        """
        Get all RAW stick values as a dictionary.

        Returns:
            raw_values: A dictionary with raw left and right stick X/Y values.
        """
        return {
            "left_stick_x": self.left_stick_x_raw(),
            "left_stick_y": self.left_stick_y_raw(),
            "right_stick_x": self.right_stick_x_raw(),
            "right_stick_y": self.right_stick_y_raw(),
        }

    def get_selection(self, options, allow_back=False):
        """
        Allows the user to navigate through a list of options and select one using left/right and A.
        The function implements a loop to display and navigate through options on the controller.
        It reacts to button presses to modify the selection index or make a selection.

        Args:
            options (list): A list of options from which the user can select.
            allow_back (bool): Flag to enable the b button to return a tuple of (did_go_back, selection) which signals whether the user exited the selection with the b button

        Returns:
            selected (Any): The selected option from the list.
        """
        selection_index = 0
        went_back = False

        wait_until_not(lambda: self.buttonA.pressing())

        def should_finish():
            return self.buttonA.pressing()

        def should_go_back():
            return self.buttonB.pressing() and allow_back

        while True:
            self.screen.clear_screen()
            self.screen.set_cursor(1, 1)
            option_name = str(
                options[selection_index]
            )  # Assuming options[selection_index] is a string.

            # Split the string into 20-character chunks.
            for i in range(0, len(option_name), 20):
                # Extract a substring of 20 characters starting from index i.
                line = option_name[i : i + 20]
                self.screen.print(line)  # Print each line.
                self.screen.next_row()  # Move to the next row after each line.

            wait_until(
                lambda: self.buttonRight.pressing()
                or self.buttonLeft.pressing()
                or should_finish()
                or should_go_back()
            )

            if should_go_back():
                went_back = True
                break

            if should_finish():
                break

            if self.buttonRight.pressing():
                selection_index += 1
            elif self.buttonLeft.pressing():
                selection_index -= 1

            wait_until_not(
                lambda: self.buttonRight.pressing() or self.buttonLeft.pressing()
            )

            if selection_index < 0:
                selection_index = 0
            elif selection_index >= len(options) - 1:
                selection_index = len(options) - 1
        wait_until_not(lambda: should_finish() or should_go_back())

        if allow_back:
            return went_back, options[selection_index]

        return options[selection_index]

    def get_multiple_selections(self, questions: list[list]):
        """
        Basically a wrapper function of get_selection, allows the user to go back to previous fields,
        we used this during robot setup to prevent the user selecting the incorrect autonomous routine from requiring us to reset the robot

        Returns:
            selected (list[Any]) The selected options in a list, in the same order they were supplied

        """
        selections = [
            options[0] for options in questions
        ]  # Select the first option for each question by default
        question_index = 0

        while True:
            pressed_back, selection = self.get_selection(questions[question_index], allow_back=True)
            selections[question_index] = selection
            if pressed_back:
                question_index -= 1
            else:
                question_index += 1

            if question_index < 0:
                question_index = 0
            elif question_index >= len(questions):
                return selections

    def get_wheel_speeds(self, control_style, drive_speed=1.0, turn_speed=1.0):
        left_speed = right_speed = 0
        if control_style == ControlStyles.TANK:
            left_speed = self.left_stick_y()
            right_speed = self.right_stick_y()
        elif control_style == ControlStyles.ARCADE:
            forward_speed = self.left_stick_y() * drive_speed
            turn_speed = self.left_stick_x() * turn_speed
            left_speed = forward_speed + turn_speed
            right_speed = forward_speed - turn_speed
        elif control_style == ControlStyles.SPLIT_ARCADE:
            forward_speed = self.left_stick_y() * drive_speed
            turn_speed = self.right_stick_x() * turn_speed
            left_speed = forward_speed + turn_speed
            right_speed = forward_speed - turn_speed

        left_speed, right_speed = desaturate_wheel_speeds([left_speed, right_speed])
        left_speed = MathUtil.clamp(left_speed, -1, 1)
        right_speed = MathUtil.clamp(right_speed, -1, 1)

        return left_speed, right_speed


class ButtonComboHandler:
    """
    Handles mapping of button combinations (simultaneous or sequential) to callbacks.
    """
    def __init__(self, controller, combo_timeout=0.3):
        """
        Args:
            controller: The vex.Controller instance.
            combo_timeout: Max time (s) between sequential presses.
        """
        self.controller = controller
        self.combo_timeout = combo_timeout
        self.combos = []  # List of (combo_def, callback)
        self.button_states = {}  # {button_name: (pressed, last_time)}
        self.event_history = collections.deque(maxlen=10)  # (button_name, time, event_type)
        self.button_map = {
            "A": controller.buttonA,
            "B": controller.buttonB,
            "X": controller.buttonX,
            "Y": controller.buttonY,
            "Up": controller.buttonUp,
            "Down": controller.buttonDown,
            "Left": controller.buttonLeft,
            "Right": controller.buttonRight,
            # Add more as needed
        }

    def add_combo(self, combo, callback, simultaneous=False):
        """
        Register a combo.
        Args:
            combo: List of button names (e.g., ["A", "B"]) for simultaneous,
                   or sequence (e.g., ["A", "B"]) for sequential.
            callback: Function to call when combo is matched.
            simultaneous: If True, combo is simultaneous; else sequential.
        """
        self.combos.append({
            "combo": combo,
            "callback": callback,
            "simultaneous": simultaneous,
        })

    def update(self):
        """
        Call this in your main loop to check for combos.
        """
        now = time.time()
        # Update button states and event history
        for name, btn in self.button_map.items():
            pressed = btn.pressing()
            prev = self.button_states.get(name, (False, 0))
            if pressed and not prev[0]:
                self.event_history.append((name, now, "down"))
                self.button_states[name] = (True, now)
            elif not pressed and prev[0]:
                self.event_history.append((name, now, "up"))
                self.button_states[name] = (False, now)
            else:
                self.button_states[name] = (pressed, prev[1])

        # Check combos
        for combo_def in self.combos:
            combo = combo_def["combo"]
            if combo_def["simultaneous"]:
                # All buttons must be pressed at the same time
                if all(self.button_map[b].pressing() for b in combo):
                    combo_def["callback"]()
            else:
                # Sequential: check event history for sequence within timeout
                idx = len(self.event_history) - 1
                matched = True
                last_time = None
                for b in reversed(combo):
                    # Find last "down" event for this button
                    while idx >= 0 and (self.event_history[idx][0] != b or self.event_history[idx][2] != "down"):
                        idx -= 1
                    if idx < 0:
                        matched = False
                        break
                    t = self.event_history[idx][1]
                    if last_time is not None and last_time - t > self.combo_timeout:
                        matched = False
                        break
                    last_time = t
                    idx -= 1
                if matched:
                    combo_def["callback"]()
