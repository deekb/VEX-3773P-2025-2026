import VEXLib.Units.Units as Units


class RotationalVelocity:
    """Represents a rotational velocity."""

    def __init__(self, velocity=0.0):
        """Initialize the RotationalVelocity object with a velocity"""
        self.velocity_radians_per_second = velocity

    def __add__(self, other):
        """Add two RotationalVelocity objects."""
        return RotationalVelocity(self.velocity_radians_per_second + other.velocity_radians_per_second)

    def __sub__(self, other):
        """Subtract two RotationalVelocity objects."""
        return RotationalVelocity(self.velocity_radians_per_second - other.velocity_radians_per_second)

    def __eq__(self, other):
        """Check if two RotationalVelocity objects are equal."""
        return self.velocity_radians_per_second == other.velocity_radians_per_second

    def __mul__(self, scalar):
        """Multiply RotationalVelocity by a scalar."""
        return RotationalVelocity(self.velocity_radians_per_second * scalar)

    def __str__(self):
        """Return the string representation of RotationalVelocity."""
        return str(self.velocity_radians_per_second) + " rad/s"

    @classmethod
    def from_radians_per_second(cls, velocity_radians_per_second):
        return cls(velocity_radians_per_second)

    @classmethod
    def from_rotations_per_second(cls, velocity_rotations_per_second):
        return cls(Units.rotations_per_second_to_radians_per_second(velocity_rotations_per_second))

    @classmethod
    def from_rotations_per_minute(cls, velocity_rotations_per_minute):
        return cls(Units.rotations_per_minute_to_radians_per_second(velocity_rotations_per_minute))

    def to_radians_per_second(self):
        return self.velocity_radians_per_second

    def to_rotations_per_second(self):
        return Units.radians_per_second_to_rotations_per_second(self.velocity_radians_per_second)

    def to_rotations_per_minute(self):
        return Units.radians_per_second_to_rotations_per_minute(self.velocity_radians_per_second)


RotSpeed = RotationalVelocity
