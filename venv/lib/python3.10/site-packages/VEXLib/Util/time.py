try:
    import utime as time_module

    IS_MICROPYTHON = True
except ImportError:
    import time as time_module

    IS_MICROPYTHON = False

from VEXLib.Units import Units


def time():
    """
    Get the current time.
    Returns:
        - MicroPython: The elapsed time since robot startup in seconds.
        - Standard Python: The current time in seconds since the epoch.
    """
    if IS_MICROPYTHON:
        return Units.milliseconds_to_seconds(time_module.ticks_ms())
    else:
        return time_module.time()


def time_ms():
    """
    Get the current time.
    Returns:
        - MicroPython: The elapsed time since robot startup in milliseconds.
        - Standard Python: The current time in milliseconds since the epoch.
    """
    if IS_MICROPYTHON:
        return time_module.ticks_ms()
    else:
        return Units.seconds_to_milliseconds(time_module.time())


def sleep(time_seconds):
    """
    Sleep for the specified amount of time in seconds.
    Works in both MicroPython and standard Python.
    """
    time_module.sleep(time_seconds)


def sleep_ms(time_milliseconds):
    """
    Sleep for the specified amount of time in milliseconds.
    Works in both MicroPython and standard Python.
    """
    time_module.sleep(Units.milliseconds_to_seconds(time_milliseconds))
