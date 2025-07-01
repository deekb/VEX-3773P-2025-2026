import unittest
from unittest.mock import patch

from VEXLib.Algorithms.RateLimiter import SlewRateLimiter


class TestSlewRateLimiter(unittest.TestCase):
    def test_slew_rate_limiter_initial_value(self):
        limiter = SlewRateLimiter(
            positive_rate_limit=1.0, negative_rate_limit=-1.0, initial_value=0.0
        )
        self.assertEqual(limiter.calculate(0.0), 0.0)

    # The @patch decorator is used to replace the 'time' function in the 'VEXLib.Algorithms.RateLimiter' module
    # with a mock object. The 'side_effect' parameter specifies a list of return values for consecutive calls
    # to the mock 'time' function. This allows us to control the passage of time in the tests without delaying the test.
    @patch("VEXLib.Algorithms.RateLimiter.time", side_effect=[0, 0.5])
    def test_slew_rate_limiter_positive_rate_limit(self, mock_time):
        limiter = SlewRateLimiter(
            positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0
        )
        result = limiter.calculate(5.0)
        self.assertTrue(0.9 <= result <= 1.1)  # Checks rate increase within limits

    @patch("VEXLib.Algorithms.RateLimiter.time", side_effect=[0, 0.5])
    def test_slew_rate_limiter_negative_rate_limit(self, mock_time):
        limiter = SlewRateLimiter(
            positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0
        )
        result = limiter.calculate(-5.0)
        self.assertTrue(-1.1 <= result <= -0.9)  # Checks rate decrease within limits

    @patch("VEXLib.Algorithms.RateLimiter.time", side_effect=[0, 0.5, 1.0])
    def test_slew_rate_limiter_reset_function(self, mock_time):
        limiter = SlewRateLimiter(
            positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0
        )
        limiter.reset(10.0)
        self.assertEqual(limiter.calculate(10.0), 10.0)

    @patch("VEXLib.Algorithms.RateLimiter.time", side_effect=[0, 0.5])
    def test_slew_rate_limiter_no_change(self, mock_time):
        limiter = SlewRateLimiter(
            positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=5.0
        )
        self.assertEqual(limiter.calculate(5.0), 5.0)


if __name__ == "__main__":
    unittest.main()
