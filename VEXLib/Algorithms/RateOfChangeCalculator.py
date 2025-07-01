class RateOfChangeCalculator:
    """
    A class to calculate the rate of change (speed) of an input over time,
    with a minimum sample time to prevent repeated calculations.
    """

    def __init__(self, minimum_sample_time: float = 0.075):
        """
        Initializes the RateOfChangeCalculator.

        :param minimum_sample_time: Minimum time (in seconds) between samples to compute rate of change.
        """
        self.min_sample_time = minimum_sample_time
        self.previous_value = None
        self.previous_time = None
        self.last_rate = 0  # Stores the last calculated rate

    def calculate_rate(self, current_value: float, current_time: float) -> float:
        """
        Calculates the rate of change of the input value over time.

        :param current_value: The current value of the input.
        :param current_time: The current time (in seconds).
        :return: The rate of change, or the last rate if insufficient time has elapsed.
        """
        if self.previous_value is None or self.previous_time is None:
            # Not enough data to calculate rate, store current inputs
            self.previous_value = current_value
            self.previous_time = current_time
            return 0  # No rate of change possible on the first call

        # Calculate time difference
        delta_time = current_time - self.previous_time

        if not self.ready_for_sample:
            # Not enough time has elapsed, return the last calculated rate
            return self.last_rate

        # Calculate delta (change in value)
        delta_value = current_value - self.previous_value

        # Compute rate of change (value/time)
        rate_of_change = delta_value / delta_time

        # Update previous values and store the calculated rate
        self.previous_value = current_value
        self.previous_time = current_time
        self.last_rate = rate_of_change

        return rate_of_change

    def ready_for_sample(self, current_time: float):
        if self.previous_value is None or self.previous_time is None:
            return True
        # Calculate time difference
        delta_time = current_time - self.previous_time

        if delta_time < self.min_sample_time:
            return False
        return True

    def reset(self):
        """
        Resets the internal state to start fresh.
        """
        self.previous_value = None
        self.previous_time = None
        self.last_rate = 0
