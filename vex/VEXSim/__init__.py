import time
from .Constants import *


def info() -> str:
    """
    Return a string with VEX Python version information.

    Returns:
        str: The VEX Python version information.
    """
    return "Simulated VEX V5 Python"


def sleep(duration: Union[int, float], units: TimeUnits.TimeUnits = TimeUnits.MSEC) -> None:
    """
    Delay the current thread for a specified number of seconds or milliseconds.

    Args:
        duration: The number of seconds or milliseconds to sleep.
        units: The units of the duration. Defaults to milliseconds.

    Returns:
        None
    """
    if units == TimeUnits.SECONDS:
        time.sleep(duration)
    else:
        time.sleep(duration / 1000)


def wait(duration: vexnumber, units=TimeUnits.MSEC):
    """Delay the current thread for the provided number of seconds or milliseconds.

    Args:
        duration: The number of seconds or milliseconds to sleep for
        units: The units of duration, optional, default is milliseconds

    Returns:
        None
    """
    if units == TimeUnits.SECONDS:
        time.sleep(duration / 1000)
    else:
        time.sleep(duration)