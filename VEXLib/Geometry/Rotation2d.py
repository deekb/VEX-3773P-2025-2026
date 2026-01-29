import math

import VEXLib.Math.MathUtil as MathUtil


class Rotation2d:
    """Represents a 2D rotation."""

    def __init__(self, angle_radians=0.0):
        """Initialize the Rotation2d object with an angle in radians."""
        self.angle_radians = angle_radians

    @staticmethod
    def _check_compatibility(other):
        """
        Checks whether the other argument is a Rotation2d object; and raises an error if not
        Args:
            other: The object to compare against

        Raises:
            ValueError
        """
        if isinstance(other, Rotation2d):
            return

        raise ValueError("Rotation2d and " + str(type(other)) +
                         " are not compatible types, please use rotation2d objects only with other rotation2d object, "
                         "to circumvent this error you can access the internal 'angle_radians' property of the rotation2d object and mutate it directly")

    def __add__(self, other):
        """Add two Rotation2d objects."""
        self._check_compatibility(other)
        return Rotation2d(self.angle_radians + other.angle_radians)

    def __sub__(self, other):
        """Subtract two Rotation2d objects."""
        self._check_compatibility(other)
        return Rotation2d(self.angle_radians - other.angle_radians)

    def __mul__(self, scalar):
        """Multiply Rotation2d by a scalar."""
        return Rotation2d(self.angle_radians * scalar)

    def __str__(self):
        """Return the string representation of Rotation2d."""
        return str(self.angle_radians) + " radians"

    def __repr__(self):
        return self.__str__()

    def sin(self):
        """Return the sine of the angle."""
        return math.sin(self.angle_radians)

    def cos(self):
        """Return the cosine of the angle."""
        return math.cos(self.angle_radians)

    def tan(self):
        """Return the tangent of the angle."""
        return math.tan(self.angle_radians)

    def atan(self):
        """Return the arctangent of the angle."""
        return math.atan(self.angle_radians)

    def sinh(self):
        """Return the hyperbolic sine of the angle."""
        return math.sinh(self.angle_radians)

    def cosh(self):
        """Return the hyperbolic cosine of the angle."""
        return math.cosh(self.angle_radians)

    def tanh(self):
        """Return the hyperbolic tangent of the angle."""
        return math.tanh(self.angle_radians)

    def asinh(self):
        """Return the inverse hyperbolic sine of the angle."""
        return math.asinh(self.angle_radians)

    def acosh(self):
        """Return the inverse hyperbolic cosine of the angle."""
        return math.acosh(self.angle_radians)

    def atanh(self):
        """Return the inverse hyperbolic tangent of the angle."""
        return math.atanh(self.angle_radians)

    @classmethod
    def from_translation2d(cls, translation2d):
        return cls.from_radians(math.atan2(translation2d.y_component.to_meters(), translation2d.x_component.to_meters()))

    @classmethod
    def from_zero(cls):
        return cls.from_radians(0)

    @classmethod
    def from_radians(cls, angle_radians):
        """Create a Rotation2d object from an angle in radians."""
        return cls(angle_radians)

    @classmethod
    def from_degrees(cls, angle_degrees):
        """Create a Rotation2d object from an angle in degrees."""
        return cls(math.radians(angle_degrees))

    @classmethod
    def from_revolutions(cls, angle_revolutions):
        """Create a Rotation2d object from an angle in revolutions."""
        return cls(angle_revolutions * 2 * math.pi)

    @classmethod
    def from_turns(cls, angle_turns):
        """Create a Rotation2d object from an angle in turns (same as revolutions)."""
        return cls.from_revolutions(angle_turns)

    def to_radians(self):
        """Return the angle in radians."""
        return self.angle_radians

    def to_degrees(self):
        """Return the angle in degrees."""
        return math.degrees(self.angle_radians)

    def to_revolutions(self):
        """Return the angle in revolutions."""
        return self.angle_radians / (2 * math.pi)

    def __truediv__(self, scalar):
        """Divide Rotation2d by a scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Rotation2d(self.angle_radians / scalar)

    def __floordiv__(self, scalar):
        """Floor division of Rotation2d by a scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Rotation2d(self.angle_radians // scalar)

    def __eq__(self, other):
        """Check if two Rotation2d objects are equal."""
        self._check_compatibility(other)
        return self.angle_radians == other.angle_radians

    def __lt__(self, other):
        """Check if the angle of Rotation2d is less than the angle of another Rotation2d."""
        return self.angle_radians < other.angle_radians

    def __le__(self, other):
        """Check if the angle of Rotation2d is less than or equal to the angle of another Rotation2d."""
        return self.angle_radians <= other.angle_radians

    def __gt__(self, other):
        """Check if the angle of Rotation2d is greater than the angle of another Rotation2d."""
        return self.angle_radians > other.angle_radians

    def __ge__(self, other):
        """Check if the angle of Rotation2d is greater than or equal to the angle of another Rotation2d."""
        return self.angle_radians >= other.angle_radians

    def interpolate(self, other, t, allow_extrapolation=True):
        """
        Perform linear interpolation between two rotations.

        Args:
            other: The Rotation2d to interpolate towards.
            t: How far between the two rotations to interpolate.
               With 0.0 corresponding to self and 1.0 corresponding to other_rotation.
            allow_extrapolation: Whether to allow the output value to go beyond the bounds of the rotations.

        Returns:
            The interpolated Rotation2d.
        """
        self._check_compatibility(other)
        return Rotation2d(
            MathUtil.interpolate(self.angle_radians, other.angle_radians, t, allow_extrapolation))

    def normalize(self):
        """
        Normalize the rotation angle to the range > -pi and <= pi radians.
        This does the right thing regardless of units
        because all values are stored as radians locally and converted when reading them

        Returns:
            The normalized Rotation2d.
        """
        return Rotation2d(MathUtil.angle_modulus(self.angle_radians))

    def inverse(self):
        return Rotation2d(-self.angle_radians)
