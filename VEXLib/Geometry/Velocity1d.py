import VEXLib.Units.Units as Units


class Velocity1d:
    """Represents a 1D velocity."""

    def __init__(self, magnitude=0.0):
        """Initialize the Velocity1d object with a velocity."""
        self.magnitude = magnitude

    def __add__(self, other):
        """Add two Velocity1d objects."""
        return Velocity1d(self.magnitude + other.magnitude)

    def __sub__(self, other):
        """Subtract two Velocity1d objects."""
        return Velocity1d(self.magnitude - other.magnitude)

    def __eq__(self, other):
        """Check if two Velocity1d objects are equal."""
        return self.magnitude == other.magnitude

    def __mul__(self, scalar):
        """Multiply Velocity1d by a scalar."""
        return Velocity1d(self.magnitude * scalar)

    def __str__(self):
        """Return the string representation of Velocity1d."""
        return str(self.magnitude) + " m/s"

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


Speed = Velocity1d
