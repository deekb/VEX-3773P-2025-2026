import time
import sys
from typing import Union
from typing import Any
from typing import Callable
from typing import List


class Ports:
    """Smartport definitions."""
    PORT1 = 0
    PORT2 = 1
    PORT3 = 2
    PORT4 = 3
    PORT5 = 4
    PORT6 = 5
    PORT7 = 6
    PORT8 = 7
    PORT9 = 8
    PORT10 = 9
    PORT11 = 10
    PORT12 = 11
    PORT13 = 12
    PORT14 = 13
    PORT15 = 14
    PORT16 = 15
    PORT17 = 16
    PORT18 = 17
    PORT19 = 18
    PORT20 = 19
    PORT21 = 20
    PORT22 = 21


class vexEnum:
    """Base class for all enumerated types."""

    def __init__(self, value: int, name: str) -> None:
        """
        Initialize vexEnum.

        Args:
            value: The integer value for the enumeration.
            name: The name of the enumeration.
        """
        self.value = value
        self.name = name

    def __str__(self) -> str:
        """Return the name of the enumeration."""
        return self.name

    def __repr__(self) -> str:
        """Return the name of the enumeration."""
        return self.name


class PercentUnits:
    """Measurement units for percentage values."""

    class PercentUnits(vexEnum):
        pass

    PERCENT = PercentUnits(0, "PERCENT")
    """A percentage unit representing a value from 0% to 100%."""


class TimeUnits:
    """Measurement units for time values."""

    class TimeUnits(vexEnum):
        pass

    SECONDS = TimeUnits(0, "SECONDS")
    """A time unit measured in seconds."""
    SEC = TimeUnits(0, "SECONDS")
    """A time unit measured in seconds."""
    MSEC = TimeUnits(1, "MSEC")
    """A time unit measured in milliseconds."""


class CurrentUnits:
    """Measurement units for current values."""

    class CurrentUnits(vexEnum):
        pass

    AMP = CurrentUnits(0, "AMP")
    """A current unit measured in amps."""


class VoltageUnits:
    """Measurement units for voltage values."""

    class VoltageUnits(vexEnum):
        pass

    VOLT = VoltageUnits(0, "VOLT")
    """A voltage unit measured in volts."""
    MV = VoltageUnits(0, "mV")
    """A voltage unit measured in millivolts."""


class PowerUnits:
    """Measurement units for power values."""

    class PowerUnits(vexEnum):
        pass

    WATT = PowerUnits(0, "WATT")
    """A power unit measured in watts."""


class TorqueUnits:
    """Measurement units for torque values."""

    class TorqueUnits(vexEnum):
        pass

    NM = TorqueUnits(0, "NM")
    """A torque unit measured in Newton Meters."""
    INLB = TorqueUnits(1, "INLB")
    """A torque unit measured in Inch Pounds."""


class RotationUnits:
    """Measurement units for rotation values."""

    class RotationUnits(vexEnum):
        pass

    DEG = RotationUnits(0, "DEG")
    """A rotation unit measured in degrees."""
    REV = RotationUnits(1, "REV")
    """A rotation unit measured in revolutions."""
    RAW = RotationUnits(99, "RAW")
    """A rotation unit measured in raw data form."""


class VelocityUnits:
    """Measurement units for velocity values."""

    class VelocityUnits(vexEnum):
        pass

    PERCENT = VelocityUnits(0, "PCT")
    """A velocity unit measured in percentage."""
    RPM = VelocityUnits(1, "RPM")
    """A velocity unit measured in rotations per minute."""
    DPS = VelocityUnits(2, "DPS")
    """A velocity unit measured in degrees per second."""


class DistanceUnits:
    """Measurement units for distance values."""

    class DistanceUnits(vexEnum):
        pass

    MM = DistanceUnits(0, "MM")
    """A distance unit measured in millimeters."""
    IN = DistanceUnits(1, "IN")
    """A distance unit measured in inches."""
    CM = DistanceUnits(2, "CM")
    """A distance unit measured in centimeters."""


class AnalogUnits:
    """Measurement units for analog values."""

    class AnalogUnits(vexEnum):
        pass

    PCT = AnalogUnits(0, "PCT")
    """An analog unit measured in percentage."""
    EIGHTBIT = AnalogUnits(0, "8BIT")
    """An analog unit measured in 8-bit analog values (256 possible states)."""
    TENBIT = AnalogUnits(0, "10BIT")
    """An analog unit measured in 10-bit analog values (1024 possible states)."""
    TWELVEBIT = AnalogUnits(0, "12BIT")
    """An analog unit measured in 12-bit analog values (4096 possible states)."""
    MV = AnalogUnits(0, "MV")
    """An analog unit measured in millivolts."""


class TemperatureUnits:
    """Measurement units for temperature values."""

    class TemperatureUnits(vexEnum):
        pass

    CELSIUS = TemperatureUnits(0, "CELSIUS")
    """A temperature unit measured in Celsius."""
    FAHRENHEIT = TemperatureUnits(0, "FAHRENHEIT")
    """A temperature unit measured in Fahrenheit."""


class DirectionType:
    """Defined units for direction values."""

    class DirectionType(vexEnum):
        pass

    FORWARD = DirectionType(0, "FORWARD")
    """A direction unit defined as forward."""
    REVERSE = DirectionType(1, "REVERSE")
    """A direction unit defined as reverse."""
    UNDEFINED = DirectionType(2, "UNDEFINED")
    """A direction unit used when direction is unknown."""


class TurnType(vexEnum):
    """Defined units for turn values."""

    class TurnType(vexEnum):
        pass

    LEFT = TurnType(0, "LEFT")
    """A turn unit defined as left."""
    RIGHT = TurnType(1, "RIGHT")
    """A turn unit defined as right."""
    UNDEFINED = TurnType(2, "UNDEFINED")
    """A turn unit used when direction is unknown."""


class BrakeType:
    """Defined units for motor brake values."""

    class BrakeType(vexEnum):
        pass

    COAST = BrakeType(0, "COAST")
    """A brake unit defined as motor coast."""
    BRAKE = BrakeType(1, "BRAKE")
    """A brake unit defined as motor brake."""
    HOLD = BrakeType(2, "HOLD")
    """A brake unit defined as motor hold."""


class GearSetting:
    """Defined units for gear values."""

    class GearSetting(vexEnum):
        pass

    RATIO_36_1 = GearSetting(0, "RATIO36_1")
    """A gear unit defined as the red 36:1 gear cartridge for V5 Smart Motors."""
    RATIO_18_1 = GearSetting(1, "RATIO18_1")
    """A gear unit defined as the green 18:1 gear cartridge for V5 Smart Motors."""
    RATIO_6_1 = GearSetting(2, "RATIO6_1")
    """A gear unit defined as the blue 6:1 gear cartridge for V5 Smart Motors."""


class FontType:
    """A unit representing font type and size."""

    class FontType(vexEnum):
        pass

    MONO20 = FontType(0, "MONO20")
    """Monotype font of size 20."""
    MONO30 = FontType(1, "MONO30")
    """Monotype font of size 30."""
    MONO40 = FontType(2, "MONO40")
    """Monotype font of size 40."""
    MONO60 = FontType(3, "MONO60")
    """Monotype font of size 60."""
    PROP20 = FontType(4, "PROP20")
    """Proportional font of size 20."""
    PROP30 = FontType(5, "PROP30")
    """Proportional font of size 30."""
    PROP40 = FontType(6, "PROP40")
    """Proportional font of size 40."""
    PROP60 = FontType(7, "PROP60")
    """Proportional font of size 60."""


def info() -> str:
    """
    Return a string with VEX Python version information.

    Returns:
        str: The VEX Python version information.
    """
    return "VEX V5 Python"


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
