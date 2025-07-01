
from VEXLib.Math import MathUtil
from time import time


class SlewRateLimiter:
    def __init__(self, positive_rate_limit, negative_rate_limit, initial_value):
        self.positive_rate_limit = positive_rate_limit  # Maximum rate of increase
        self.negative_rate_limit = negative_rate_limit  # Maximum rate of decrease
        self.previous_value = initial_value  # Initial value for rate limiter
        self.previous_time = time()  # Timestamp of the last calculation

    def calculate(self, input_value):
        current_time = time()
        elapsed_time = current_time - self.previous_time  # Time difference

        self.previous_value += MathUtil.clamp(
            input_value - self.previous_value,
            self.negative_rate_limit * elapsed_time,
            self.positive_rate_limit * elapsed_time,
        )

        self.previous_time = current_time  # Update the previous timestamp

        return self.previous_value

    def reset(self, value):
        self.previous_value = value  # Reset rate limiter to a new value

        self.previous_time = time()  # Reset the time reference
