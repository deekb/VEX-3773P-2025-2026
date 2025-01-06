import time
import unittest
from VEXLib.Algorithms.RateLimiter import SlewRateLimiter


class TestSlewRateLimiter(unittest.TestCase):
    def test_slew_rate_limiter_initial_value(self):
        limiter = SlewRateLimiter(positive_rate_limit=1.0, negative_rate_limit=-1.0, initial_value=0.0)
        self.assertEqual(limiter.calculate(0.0), 0.0)

    def test_slew_rate_limiter_positive_rate_limit(self):
        limiter = SlewRateLimiter(positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0)
        time.sleep(0.5)  # Simulate time passing
        result = limiter.calculate(5.0)
        self.assertTrue(0.9 <= result <= 1.1)  # Checks rate increase within limits

    def test_slew_rate_limiter_negative_rate_limit(self):
        limiter = SlewRateLimiter(positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0)
        time.sleep(0.5)  # Simulate time passing
        result = limiter.calculate(-5.0)
        self.assertTrue(-1.1 <= result <= -0.9)  # Checks rate decrease within limits

    def test_slew_rate_limiter_reset_function(self):
        limiter = SlewRateLimiter(positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=0.0)
        limiter.reset(10.0)
        self.assertEqual(limiter.calculate(10.0), 10.0)

    def test_slew_rate_limiter_no_change(self):
        limiter = SlewRateLimiter(positive_rate_limit=2.0, negative_rate_limit=-2.0, initial_value=5.0)
        time.sleep(0.5)  # Simulate time passing
        self.assertEqual(limiter.calculate(5.0), 5.0)


if __name__ == '__main__':
    unittest.main()