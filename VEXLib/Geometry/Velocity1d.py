import VEXLib.Units.Units as Units
from VEXLib.Geometry.Constants import VELOCITY1D_IDENTIFIER


class Velocity1d:
    """Represents a 1D velocity."""

    def __init__(self, magnitude=0.0):
        """Initialize the Velocity1d object with a velocity."""
        self.magnitude = magnitude

    def __add__(self, other):
        """Add two Velocity1d objects."""
        return Velocity1d(self.magnitude + other.magnitude)

    def __radd__(self, other):
        """Add two Velocity1d objects."""
        return self.__add__(other)

    def __iadd__(self, other):
        """In-place addition of two Velocity1d objects."""
        self.magnitude += other.magnitude
        return self

    def __sub__(self, other):
        """Subtract two Velocity1d objects."""
        return Velocity1d(self.magnitude - other.magnitude)

    def __rsub__(self, other):
        """Reverse subtract two Velocity1d objects."""
        return Velocity1d(other.magnitude - self.magnitude)

    def __isub__(self, other):
        """In-place subtraction of two Velocity1d objects."""
        self.magnitude -= other.magnitude
        return self

    def __mul__(self, scalar):
        """Multiply Velocity1d by a scalar."""
        return Velocity1d(self.magnitude * scalar)

    def __rmul__(self, scalar):
        """Reverse multiply Velocity1d by a scalar."""
        return self.__mul__(scalar)

    def __imul__(self, scalar):
        """In-place multiplication of Velocity1d by a scalar."""
        self.magnitude *= scalar
        return self

    def __truediv__(self, scalar):
        """Divide Velocity1d by a scalar."""
        return Velocity1d(self.magnitude / scalar)

    def __rtruediv__(self, scalar):
        """Reverse divide Velocity1d by a scalar."""
        return Velocity1d(scalar / self.magnitude)

    def __itruediv__(self, scalar):
        """In-place division of Velocity1d by a scalar."""
        self.magnitude /= scalar
        return self

    def __eq__(self, other):
        """Check if two Velocity1d objects are equal."""
        return self.magnitude == other.magnitude

    def __str__(self):
        """Return the string representation of Velocity1d."""
        return "Velocity1d<" + str(self.magnitude) + " m/s>"

    def __repr__(self):
        """Return the string representation of Velocity1d."""
        return self.__str__()

    @classmethod
    def from_meters_per_second(cls, x_meters_per_second):
        return cls(x_meters_per_second)

    @classmethod
    def from_centimeters_per_second(cls, x_centimeters_per_second):
        return cls(Units.centimeters_to_meters(x_centimeters_per_second))

    @classmethod
    def from_inches_per_second(cls, x_inches_per_second):
        return cls(Units.inches_to_meters(x_inches_per_second))

    @classmethod
    def from_feet_per_second(cls, x_feet_per_second):
        return cls(Units.feet_to_meters(x_feet_per_second))

    def to_meters_per_second(self):
        return self.magnitude

    def to_centimeters_per_second(self):
        return Units.meters_to_centimeters(self.magnitude)

    def to_inches_per_second(self):
        return Units.meters_to_inches(self.magnitude)

    def to_bytestring(self, include_identifier=True):
        """Return a compressed bytestring representing the Velocity2d in meters per second."""
        return (VELOCITY1D_IDENTIFIER if include_identifier else b"") + float(self.magnitude).hex().encode()

    @classmethod
    def from_bytestring(cls, bytestring, include_identifier=True):
        """Create a Velocity2d object from a compressed bytestring."""
        if include_identifier:
            if not bytestring.startswith(VELOCITY1D_IDENTIFIER):
                raise ValueError("Invalid bytestring for Velocity1d, must start with " + str(VELOCITY1D_IDENTIFIER))
            bytestring = bytestring[len(VELOCITY1D_IDENTIFIER):]
        magnitude = float.fromhex(bytestring.decode())
        return cls(magnitude)


Speed = Velocity1d