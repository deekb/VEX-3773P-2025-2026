import math

from VEXLib.Geometry.Constants import VELOCITY2D_IDENTIFIER, SEPERATOR
from VEXLib.Geometry.Velocity1d import Velocity1d
from VEXLib.Math import MathUtil


class Velocity2d:
    """Represents a 2D velocity."""

    def __init__(self, x_component: Velocity1d = Velocity1d(), y_component: Velocity1d = Velocity1d()):
        """Initialize the Velocity2d object with x and y speeds"""
        self.x_component = x_component
        self.y_component = y_component

    def __add__(self, other):
        """Add two Velocity2d objects."""
        return Velocity2d(self.x_component + other.x_component, self.y_component + other.y_component)

    def __radd__(self, other):
        """Add two Velocity2d objects."""
        return self.__add__(other)

    def __iadd__(self, other):
        """In-place addition of two Velocity2d objects."""
        self.x_component += other.x_component
        self.y_component += other.y_component
        return self

    def __sub__(self, other):
        """Subtract two Velocity2d objects."""
        return Velocity2d(self.x_component - other.x_component, self.y_component - other.y_component)

    def __rsub__(self, other):
        """Reverse subtract two Velocity2d objects."""
        return Velocity2d(other.x_component - self.x_component, other.y_component - self.y_component)

    def __isub__(self, other):
        """In-place subtraction of two Velocity2d objects."""
        self.x_component -= other.x_component
        self.y_component -= other.y_component
        return self

    def __mul__(self, scalar):
        """Multiply Velocity2d by a scalar."""
        return Velocity2d(self.x_component * scalar, self.y_component * scalar)

    def __rmul__(self, scalar):
        """Reverse multiply Velocity2d by a scalar."""
        return self.__mul__(scalar)

    def __imul__(self, scalar):
        """In-place multiplication of Velocity2d by a scalar."""
        self.x_component *= scalar
        self.y_component *= scalar
        return self

    def __truediv__(self, scalar):
        """Divide Velocity2d by a scalar."""
        return Velocity2d(self.x_component / scalar, self.y_component / scalar)

    def __rtruediv__(self, scalar):
        """Reverse divide Velocity2d by a scalar."""
        return Velocity2d(scalar / self.x_component, scalar / self.y_component)

    def __itruediv__(self, scalar):
        """In-place division of Velocity2d by a scalar."""
        self.x_component /= scalar
        self.y_component /= scalar
        return self

    def __eq__(self, other):
        """Check if two Velocity2d objects are equal."""
        return self.x_component == other.x_component and self.y_component == other.y_component

    def __str__(self):
        """Return the string representation of Velocity2d."""
        return "(" + str(self.x_component) + ", " + str(self.y_component) + ")"

    def __repr__(self):
        """Return the string representation of Velocity2d."""
        return self.__str__()

    @classmethod
    def from_meters_per_second(cls, x_meters_per_second, y_meters_per_second):
        return cls(Velocity1d.from_meters_per_second(x_meters_per_second), Velocity1d.from_meters_per_second(y_meters_per_second))

    @classmethod
    def from_centimeters_per_second(cls, x_centimeters_per_second, y_centimeters_per_second):
        return cls(Velocity1d.from_centimeters_per_second(x_centimeters_per_second),
                   Velocity1d.from_centimeters_per_second(y_centimeters_per_second))

    @classmethod
    def from_inches_per_second(cls, x_inches_per_second, y_inches_per_second):
        return cls(Velocity1d.from_inches_per_second(x_inches_per_second),
                   Velocity1d.from_inches_per_second(y_inches_per_second))

    @classmethod
    def from_feet_per_second(cls, x_feet_per_second, y_feet_per_second):
        return cls(Velocity1d.from_feet_per_second(x_feet_per_second),
                   Velocity1d.from_feet_per_second(y_feet_per_second))

    def to_meters_per_second(self):
        return self.x_component.to_meters_per_second(), self.y_component.to_meters_per_second()

    def to_centimeters_per_second(self):
        return self.x_component.to_centimeters_per_second(), self.y_component.to_centimeters_per_second()

    def to_inches_per_second(self):
        return self.x_component.to_inches_per_second(), self.y_component.to_inches_per_second()

    @property
    def angle_rad(self):
        return math.atan2(self.y_component.to_meters_per_second(), self.x_component.to_meters_per_second())

    @angle_rad.setter
    def angle_rad(self, angle):
        length = self.get_length()
        self.x_component = length * math.cos(angle)
        self.y_component = length * math.sin(angle)

    def get_length(self):
        return Velocity1d.from_meters_per_second(MathUtil.hypotenuse(self.x_component.to_meters_per_second(), self.y_component.to_meters_per_second()))

    def to_bytestring(self, include_identifier=True):
        """Return a compressed bytestring representing the Velocity2d in meters per second."""
        x_bytes = self.x_component.to_bytestring(include_identifier=False)
        y_bytes = self.y_component.to_bytestring(include_identifier=False)
        return (VELOCITY2D_IDENTIFIER if include_identifier else b"") + x_bytes + SEPERATOR + y_bytes

    @classmethod
    def from_bytestring(cls, bytestring):
        """Create a Velocity2d object from a compressed bytestring."""
        if not bytestring.startswith(VELOCITY2D_IDENTIFIER):
            raise ValueError("Invalid bytestring for Velocity2d, must start with " + str(VELOCITY2D_IDENTIFIER))
        x_str, y_str = bytestring[len(VELOCITY2D_IDENTIFIER):].split(SEPERATOR)
        x_magnitude = Velocity1d.from_bytestring(x_str, include_identifier=False)
        y_magnitude = Velocity1d.from_bytestring(y_str, include_identifier=False)
        return cls(x_magnitude, y_magnitude)


Speed2d = Velocity2d