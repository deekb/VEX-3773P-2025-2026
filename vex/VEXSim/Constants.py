from typing import Union


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


class ThreeWireType:
    """The defined units for 3-wire devices."""

    class ThreeWireType(vexEnum):
        pass

    ANALOG_IN = ThreeWireType(0, "ANALOG_IN")
    """A 3-wire sensor that is defined as an analog input."""
    ANALOG_OUT = ThreeWireType(1, "ANALOG_OUT")
    """A 3-wire sensor that is defined as an analog output."""
    DIGITAL_IN = ThreeWireType(2, "DIGITAL_IN")
    """A 3-wire sensor that is defined as an digital input."""
    DIGITAL_OUT = ThreeWireType(3, "DIGITAL_OUT")
    """A 3-wire sensor that is defined as an digital output."""
    SWITCH = ThreeWireType(4, "BUTTON")
    """A 3-wire sensor that is defined as a switch."""
    POTENTIOMETER = ThreeWireType(5, "POT")
    """A 3-wire sensor that is defined as a potentiometer."""
    LINE_SENSOR = ThreeWireType(6, "LINE_SENSOR")
    """A 3-wire sensor that is defined as a line sensor."""
    LIGHT_SENSOR = ThreeWireType(7, "LIGHT_SENSOR")
    """A 3-wire sensor that is defined as a light sensor."""
    GYRO = ThreeWireType(8, "GYRO")
    """A 3-wire sensor that is defined as a yaw rate gyro."""
    ACCELEROMETER = ThreeWireType(9, "ACCELEROMETER")
    """A 3-wire sensor that is defined as a accelerometer."""
    MOTOR = ThreeWireType(10, "MOTOR")
    """A 3-wire sensor that is defined as a legacy vex motor."""
    SERVO = ThreeWireType(11, "SERVO")
    """A 3-wire sensor that is defined as a legacy vex servo."""
    ENCODER = ThreeWireType(12, "ENCODER")
    """A 3-wire sensor that is defined as a quadrature encoder."""
    SONAR = ThreeWireType(13, "SONAR")
    """A 3-wire sensor that is defined as an ultrasonic sensor (sonar)"""
    SLEW_MOTOR = ThreeWireType(14, "SLEW_MOTOR")
    """A 3-wire sensor that is defined as a legacy vex motor using slew rate control."""


class ControllerType:
    """The defined types for controller devices."""

    class ControllerType(vexEnum):
        pass

    PRIMARY = ControllerType(0, "PRIMARY")
    """A controller defined as a primary controller."""
    PARTNER = ControllerType(1, "PARTNER")
    """A controller defined as a partner controller."""


class AxisType:
    """The defined units for inertial sensor axis."""

    class AxisType(vexEnum):
        pass

    XAXIS = AxisType(0, "XAXIS")
    """The X axis of the Inertial sensor."""
    YAXIS = AxisType(1, "YAXIS")
    """The Y axis of the Inertial sensor."""
    ZAXIS = AxisType(2, "ZAXIS")
    """The Z axis of the Inertial sensor."""


class OrientationType:
    """The defined units for inertial sensor orientation."""

    class OrientationType(vexEnum):
        pass

    ROLL = OrientationType(0, "ROLL")
    """roll, orientation around the X axis of the Inertial sensor."""
    PITCH = OrientationType(1, "PITCH")
    """pitch, orientation around the Y axis of the Inertial sensor."""
    YAW = OrientationType(2, "YAW")
    """yaw, orientation around the Z axis of the Inertial sensor."""


class ObjectSizeType:
    """The defined units for distance sensor object size."""

    class ObjectSizeType(vexEnum):
        pass

    NONE = ObjectSizeType(0, "NONE")
    SMALL = ObjectSizeType(1, "SMALL")
    MEDIUM = ObjectSizeType(2, "MEDIUM")
    LARGE = ObjectSizeType(3, "LARGE")


class LedStateType:
    """The defined units for optical sensor led state."""

    class LedStateType(vexEnum):
        pass

    OFF = LedStateType(0, "OFF")
    ON = LedStateType(1, "ON")
    BLINK = LedStateType(2, "BLINK")


class GestureType:
    """The defined units for optical sensor gesture types."""

    class GestureType(vexEnum):
        pass

    NONE = GestureType(0, "NONE")
    UP = GestureType(1, "UP")
    DOWN = GestureType(2, "DOWN")
    LEFT = GestureType(3, "LEFT")
    RIGHT = GestureType(4, "RIGHT")


class VexlinkType:
    """The defined units for vexlink types."""

    class VexlinkType(vexEnum):
        pass

    MANAGER = VexlinkType(1, "MANAGER")
    """A vexlink type that is defined as the manager radio."""
    WORKER = VexlinkType(2, "WORKER")
    """A vexlink type that is defined as the worker radio."""
    GENERIC = VexlinkType(3, "GENERIC")
    """A vexlink type that is defined as a raw unmanaged link."""


PERCENT = PercentUnits.PERCENT
"""A percentage unit that represents a value from 0% to 100%"""
FORWARD = DirectionType.FORWARD
"""A direction unit that is defined as forward."""
REVERSE = DirectionType.REVERSE
"""A direction unit that is defined as backward."""
LEFT = TurnType.LEFT
"""A turn unit that is defined as left turning."""
RIGHT = TurnType.LEFT
"""A turn unit that is defined as right turning."""
DEGREES = RotationUnits.DEG
"""A rotation unit that is measured in degrees."""
TURNS = RotationUnits.REV
"""A rotation unit that is measured in revolutions."""
RPM = VelocityUnits.RPM
"""A velocity unit that is measured in rotations per minute."""
DPS = VelocityUnits.DPS
"""A velocity unit that is measured in degrees per second."""
SECONDS = TimeUnits.SECONDS
"""A time unit that is measured in seconds."""
MSEC = TimeUnits.MSEC
"""A time unit that is measured in milliseconds."""
INCHES = DistanceUnits.IN
"""A distance unit that is measured in inches."""
MM = DistanceUnits.MM
"""A distance unit that is measured in millimeters."""
XAXIS = AxisType.XAXIS
"""The X axis of the Inertial sensor."""
YAXIS = AxisType.YAXIS
"""The Y axis of the Inertial sensor."""
ZAXIS = AxisType.ZAXIS
"""The Z axis of the Inertial sensor."""
ROLL = OrientationType.ROLL
"""roll, orientation around the X axis of the Inertial sensor."""
PITCH = OrientationType.PITCH
"""pitch, orientation around the Y axis of the Inertial sensor."""
YAW = OrientationType.YAW
"""yaw, orientation around the Z axis of the Inertial sensor."""
PRIMARY = ControllerType.PRIMARY
"""A controller defined as a primary controller."""
PARTNER = ControllerType.PARTNER
"""A controller defined as a partner controller."""
COAST = BrakeType.COAST
"""A brake unit that is defined as motor coast."""
BRAKE = BrakeType.BRAKE
"""A brake unit that is defined as motor brake."""
HOLD = BrakeType.HOLD
"""A brake unit that is defined as motor hold."""
VOLT = VoltageUnits.VOLT
"""A voltage unit that is measured in volts."""
MV = VoltageUnits.MV
"""A voltage unit that is measured in millivolts."""

# most functions will take number in either format
vexnumber = Union[int, float]
VelocityPercentUnits = Union[VelocityUnits.VelocityUnits, PercentUnits.PercentUnits]
TorquePercentUnits = Union[TorqueUnits.TorqueUnits, PercentUnits.PercentUnits]
TorquePercentCurrentUnits = Union[TorqueUnits.TorqueUnits, PercentUnits.PercentUnits, CurrentUnits.CurrentUnits]
TemperaturePercentUnits = Union[TemperatureUnits.TemperatureUnits, PercentUnits.PercentUnits]
AnalogPercentUnits = Union[AnalogUnits.AnalogUnits, PercentUnits.PercentUnits]
RotationPercentUnits = Union[RotationUnits.RotationUnits, PercentUnits.PercentUnits]
RotationTimeUnits = Union[RotationUnits.RotationUnits, TimeUnits.TimeUnits]
