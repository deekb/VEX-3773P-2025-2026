from VEXLib.Math import MathUtil
from VEXLib.Util.CircularBuffer import CircularBuffer


class MovingWindowAverage:
    """
    A class to handle moving window average operations.
    """

    def __init__(self, buffer: CircularBuffer):
        """
        Initializes the MovingWindowAverage with a buffer to hold the values.
        """
        self.buffer = buffer

    def add_value(self, value):
        """
        Adds a value to the window and calculates the smoothed average.

        :param value: The new value to add to the window.
        :return: The current smoothed average based on the window.
        """
        self.buffer.add(value)
        return self.get_average()

    def get_average(self):
        """
        Calculates the average of the current window.

        :return: The average of the current window
        """
        return MathUtil.average_iterable(self.buffer.get())

    def reset(self):
        """
        Resets the values in the window for reuse.
        """
        self.buffer.clear()
