from VEXLib.Math import MathUtil


class MovingWindowAverage:
    """
    A class to handle moving window average operations.
    """

    def __init__(self, window_size):
        """
        Initializes the MovingWindowAverage with a specified window size.

        :param window_size: The number of elements in the moving window.
        """
        self.window_size = window_size
        self.values = [0] * window_size
        self.index = 0
        self.count = 0

    def add_value(self, value):
        """
        Adds a value to the window and calculates the smoothed average.

        :param value: The new value to add to the window.
        :return: The current smoothed average based on the window.
        """
        self.values[self.index] = value
        self.index = (self.index + 1) % self.window_size
        if self.count < self.window_size:
            self.count += 1

        return self.get_average()

    def get_average(self):
        """
        Calculates the average of the current window.

        :return: The average of the current window, or 0 if the window is empty.
        """
        if self.count == 0:
            return 0

        return MathUtil.average_iterable(self.values[:self.count])

    def reset(self):
        """
        Resets the values in the window for reuse.
        """
        self.values = [0] * self.window_size
        self.index = 0
        self.count = 0