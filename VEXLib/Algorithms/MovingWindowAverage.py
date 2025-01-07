from VEXLib.Math import MathUtil


class MovingWindowAverage:
    """
    A class to handle moving window average operations.
    """

    def __init__(self, window_size: int):
        """
        Initializes the MovingWindowAverage with a specified window size.

        :param window_size: The number of elements in the moving window.
        """
        self.window_size = window_size
        self.values = []

    def add_value(self, value: float) -> float:
        """
        Adds a value to the window and calculates the smoothed average.

        :param value: The new value to add to the window.
        :return: The current smoothed average based on the window.
        """
        self.values.append(value)

        # Keep the window size limited to the specified size
        if len(self.values) > self.window_size:
            self.values.pop(0)

        # Calculate and return the average
        return self.get_average()

    def get_average(self) -> float:
        """
        Calculates the average of the current window.

        :return: The average of the current window, or 0 if the window is empty.
        """
        if not self.values:
            return 0

        return MathUtil.average_iterable(self.values)

    def reset(self):
        """
        Resets the values in the window for reuse.
        """
        self.values = []
