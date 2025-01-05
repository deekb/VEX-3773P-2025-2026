try:
    # Try to import MicroPython library
    import utime as _time
except ImportError:
    # Fallback to standard Python library
    import time as _time

from VEXLib.Units import Units

# Define constants
MAX_TIMER_VALUE = (2 ** 31) // 2
continuous_time_us = 0
prev_timer_value_us = 0


class TimeUtils:
    """Utility class to abstract time functions for compatibility."""

    @staticmethod
    def raw_time_us():
        """
        Function to get the current timer value in microseconds.
        Returns the timer ticks similar to `utime.ticks_us()`.
        """
        if hasattr(_time, 'ticks_us'):
            return _time.ticks_us()  # MicroPython function
        else:
            # Approximate for standard Python using time.time()
            return int(_time.time() * 1_000_000)

    @staticmethod
    def sleep(seconds):
        """Sleep for the specified number of seconds."""
        _time.sleep(seconds)

    @staticmethod
    def sleep_ms(milliseconds):
        """
        Sleep for the specified number of milliseconds using Units for conversion.
        Converts milliseconds to seconds before calling sleep().
        """
        seconds = Units.milliseconds_to_seconds(milliseconds)
        _time.sleep(seconds)


def time():
    """
    Get the current timestamp in seconds since the program started.
    Handles rollover of timer values for continuous time tracking.
    """
    global continuous_time_us, prev_timer_value_us

    current_timer_value = TimeUtils.raw_time_us()

    if current_timer_value < prev_timer_value_us:
        # Handle timer wraparound
        delta = (MAX_TIMER_VALUE - prev_timer_value_us) + current_timer_value
        print("Timer wraparound: Compensating using continuous timer...")
    else:
        # Normal time progression
        delta = current_timer_value - prev_timer_value_us

    # Update continuous time with the delta
    continuous_time_us += delta
    prev_timer_value_us = current_timer_value

    # Convert to seconds using Units and return
    return Units.microseconds_to_seconds(continuous_time_us)


def time_ms():
    """
    Get the current timestamp in milliseconds since the program started.
    Similar to `time()` but returns the value in milliseconds.
    """
    global continuous_time_us, prev_timer_value_us

    current_timer_value = TimeUtils.raw_time_us()

    if current_timer_value < prev_timer_value_us:
        # Handle timer wraparound
        delta = (MAX_TIMER_VALUE - prev_timer_value_us) + current_timer_value
        print("Timer wraparound: Compensating using continuous timer...")
    else:
        # Normal time progression
        delta = current_timer_value - prev_timer_value_us

    # Update continuous time with the delta
    continuous_time_us += delta
    prev_timer_value_us = current_timer_value

    # Convert to milliseconds using Units and return
    return Units.microseconds_to_milliseconds(continuous_time_us)


def sleep(time_seconds):
    """
    Sleep for the specified number of seconds.
    This wraps the platform-agnostic sleep logic from TimeUtils.
    """
    TimeUtils.sleep(time_seconds)
