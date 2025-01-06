from VEXLib.Units import Units


class Translation1d:
    """Represents a 1D translation."""

    def __init__(self, magnitude=0):
        """Initialize the Translation1d object with a one-dimensional magnitude.

        Args:
            magnitude (float): The magnitude. Defaults to 0.
        """
        self.magnitude = magnitude

    def __add__(self, other):
        """Add two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to add.

        Returns:
            Translation1d: A new Translation1d object with the summed magnitudes.
        """
        return Translation1d(self.magnitude + other.magnitude)

    def __sub__(self, other):
        """Subtract two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to subtract.

        Returns:
            Translation1d: A new Translation1d object with the subtracted magnitudes.
        """
        return Translation1d(self.magnitude - other.magnitude)

    def __eq__(self, other):
        """Check if two Translation1d objects are equal.

        Args:
            other (Translation1d): The other Translation1d object to compare.

        Returns:
            bool: True if the x coordinates are equal, False otherwise.
        """
        return self.magnitude == other.magnitude

    def __mul__(self, scalar):
        """Multiply Translation1d by a scalar.

        Args:
            scalar (float): The scalar to multiply with.

        Returns:
            Translation1d: A new Translation1d object with the scaled x coordinate.
        """
        return Translation1d(self.magnitude * scalar)

    def __truediv__(self, scalar):
        """Divide Translation1d by a scalar.

        Args:
            scalar (float): The scalar to divide with.

        Returns:
            Translation1d: A new Translation1d object with the scaled x coordinate.
        """
        return Translation1d(self.magnitude / scalar)

    def __str__(self):
        """Return the string representation of Translation1d.

        Returns:
            str: The string representation of the x coordinate.
        """
        return str(self.magnitude) + "m"

    @classmethod
    def from_meters(cls, x_meters):
        """Create a Translation1d object from meters.

        Args:
            x_meters (float): The x coordinate in meters.

        Returns:
            Translation1d: A new Translation1d object with the x coordinate in meters.
        """
        return cls(x_meters)

    @classmethod
    def from_centimeters(cls, x_centimeters):
        """Create a Translation1d object from centimeters.

        Args:
            x_centimeters (float): The x coordinate in centimeters.

        Returns:
            Translation1d: A new Translation1d object with the x coordinate converted to meters.
        """
        return cls(Units.centimeters_to_meters(x_centimeters))

    @classmethod
    def from_inches(cls, x_inches):
        """Create a Translation1d object from inches.

        Args:
            x_inches (float): The x coordinate in inches.

        Returns:
            Translation1d: A new Translation1d object with the x coordinate converted to meters.
        """
        return cls(Units.inches_to_meters(x_inches))

    @classmethod
    def from_feet(cls, x_feet):
        """Create a Translation1d object from feet.

        Args:
            x_feet (float): The x coordinate in feet.

        Returns:
            Translation1d: A new Translation1d object with the x coordinate converted to meters.
        """
        return cls(Units.feet_to_meters(x_feet))

    def to_meters(self):
        """Convert the x coordinate to meters.

        Returns:
            float: The x coordinate in meters.
        """
        return self.magnitude

    def to_centimeters(self):
        """Convert the x coordinate to centimeters.

        Returns:
            float: The x coordinate in centimeters.
        """
        return Units.meters_to_centimeters(self.magnitude)

    def to_inches(self):
        """Convert the x coordinate to inches.

        Returns:
            float: The x coordinate in inches.
        """
        return Units.meters_to_inches(self.magnitude)

    def to_feet(self):
        """Convert the x coordinate to feet.

        Returns:
            float: The x coordinate in feet.
        """
        return Units.meters_to_feet(self.magnitude)

    def inverse(self):
        """
        Calculates the unary inverse of a translation1d object, equivalent to inverting the sign (rotating it by a half-turn)
        Returns:
            A rotation1d object that is the original translation with the sign inverted

        """
        return Translation1d(-self.magnitude)


# Alias Translation1d as Distance
Distance = Translation1d
