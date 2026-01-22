from VEXLib.Geometry.Constants import TRANSLATION1D_IDENTIFIER
from VEXLib.Units import Units


class Translation1d:
    """Represents a 1D translation."""

    def __init__(self, magnitude=0.0):
        """
        Initialize the Translation1d object with a one-dimensional magnitude.

        Args:
            magnitude (float): The magnitude. Defaults to 0.0.
        """
        self.magnitude = magnitude

    def __add__(self, other):
        """
        Add two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to add.

        Returns:
            Translation1d: A new Translation1d object with the summed magnitudes.
        """
        return Translation1d(self.magnitude + other.magnitude)

    def __radd__(self, other):
        """
        Add two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to add.

        Returns:
            Translation1d: A new Translation1d object with the summed magnitudes.
        """
        return Translation1d(self.magnitude + other.magnitude)

    def __iadd__(self, other):
        """
        In-place addition of two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to add.

        Returns:
            Translation1d: The updated Translation1d object.
        """
        self.magnitude += other.magnitude
        return self

    def __sub__(self, other):
        """
        Subtract two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to subtract.

        Returns:
            Translation1d: A new Translation1d object with the subtracted magnitudes.
        """
        return Translation1d(self.magnitude - other.magnitude)

    def __rsub__(self, other):
        """
        Reverse subtract two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to subtract.

        Returns:
            Translation1d: A new Translation1d object with the subtracted magnitudes.
        """
        return Translation1d(other.magnitude - self.magnitude)

    def __isub__(self, other):
        """
        In-place subtraction of two Translation1d objects.

        Args:
            other (Translation1d): The other Translation1d object to subtract.

        Returns:
            Translation1d: The updated Translation1d object.
        """
        self.magnitude -= other.magnitude
        return self

    def __mul__(self, scalar):
        """
        Multiply Translation1d by a scalar.

        Args:
            scalar (float): The scalar to multiply with.

        Returns:
            Translation1d: A new Translation1d object with the scaled magnitude.
        """
        return Translation1d(self.magnitude * scalar)

    def __rmul__(self, scalar):
        """
        Reverse multiply Translation1d by a scalar.

        Args:
            scalar (float): The scalar to multiply with.

        Returns:
            Translation1d: A new Translation1d object with the scaled magnitude.
        """
        return Translation1d(self.magnitude * scalar)

    def __imul__(self, scalar):
        """
        In-place multiplication of Translation1d by a scalar.

        Args:
            scalar (float): The scalar to multiply with.

        Returns:
            Translation1d: The updated Translation1d object.
        """
        self.magnitude *= scalar
        return self

    def __truediv__(self, scalar):
        """
        Divide Translation1d by a scalar.

        Args:
            scalar (float): The scalar to divide with.

        Returns:
            Translation1d: A new Translation1d object with the scaled magnitude.
        """
        return Translation1d(self.magnitude / scalar)

    def __rtruediv__(self, scalar):
        """
        Reverse divide Translation1d by a scalar.

        Args:
            scalar (float): The scalar to divide with.

        Returns:
            Translation1d: A new Translation1d object with the scaled magnitude.
        """
        return Translation1d(scalar / self.magnitude)

    def __itruediv__(self, scalar):
        """
        In-place division of Translation1d by a scalar.

        Args:
            scalar (float): The scalar to divide with.

        Returns:
            Translation1d: The updated Translation1d object.
        """
        self.magnitude /= scalar
        return self

    def __eq__(self, other):
        """
        Check if two Translation1d objects are equal.

        Args:
            other (Translation1d): The other Translation1d object to compare.

        Returns:
            bool: True if the magnitudes are equal, False otherwise.
        """
        return self.magnitude == other.magnitude

    def __str__(self):
        """
        Return the string representation of Translation1d.

        Returns:
            str: The string representation of the magnitude.
        """
        return str(self.magnitude) + "m"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_zero(cls):
        """
        Create a Translation1d object with a magnitude of zero.

        Returns:
            Translation1d: A new Translation1d object with a magnitude of zero.
        """
        return cls(0.0)

    @classmethod
    def from_meters(cls, x_meters):
        """
        Create a Translation1d object from meters.

        Args:
            x_meters (float): The magnitude in meters.

        Returns:
            Translation1d: A new Translation1d object with the magnitude in meters.
        """
        return cls(x_meters)

    @classmethod
    def from_millimeters(cls, x_millimeters):
        """
        Create a Translation1d object from millimeters.

        Args:
            x_millimeters (float): The magnitude in millimeters.

        Returns:
            Translation1d: A new Translation1d object with the magnitude in millimeters.
        """
        return cls(Units.millimeters_to_meters(x_millimeters))

    @classmethod
    def from_centimeters(cls, x_centimeters):
        """
        Create a Translation1d object from centimeters.

        Args:
            x_centimeters (float): The magnitude in centimeters.

        Returns:
            Translation1d: A new Translation1d object with the magnitude converted to meters.
        """
        return cls(Units.centimeters_to_meters(x_centimeters))

    @classmethod
    def from_inches(cls, x_inches):
        """
        Create a Translation1d object from inches.

        Args:
            x_inches (float): The magnitude in inches.

        Returns:
            Translation1d: A new Translation1d object with the magnitude converted to meters.
        """
        return cls(Units.inches_to_meters(x_inches))

    @classmethod
    def from_feet(cls, x_feet):
        """
        Create a Translation1d object from feet.

        Args:
            x_feet (float): The magnitude in feet.

        Returns:
            Translation1d: A new Translation1d object with the magnitude converted to meters.
        """
        return cls(Units.feet_to_meters(x_feet))

    def to_meters(self):
        """
        Convert the magnitude to meters.

        Returns:
            float: The magnitude in meters.
        """
        return self.magnitude

    def to_centimeters(self):
        """
        Convert the magnitude to centimeters.

        Returns:
            float: The magnitude in centimeters.
        """
        return Units.meters_to_centimeters(self.magnitude)

    def to_inches(self):
        """
        Convert the magnitude to inches.

        Returns:
            float: The magnitude in inches.
        """
        return Units.meters_to_inches(self.magnitude)

    def to_feet(self):
        """
        Convert the magnitude to feet.

        Returns:
            float: The magnitude in feet.
        """
        return Units.meters_to_feet(self.magnitude)

    def inverse(self):
        """
        Calculate the unary inverse of a Translation1d object.

        Returns:
            Translation1d: A new Translation1d object with the sign of the magnitude inverted.
        """
        return Translation1d(-self.magnitude)

    def to_bytestring(self, include_identifier=True):
        """
        Return a compressed bytestring representing the Translation1d in meters.

        Args:
            include_identifier (bool): Whether to include the identifier in the bytestring. Defaults to True.

        Returns:
            bytes: The compressed bytestring.
        """
        return (TRANSLATION1D_IDENTIFIER if include_identifier else b"") + float(self.magnitude).hex().encode()

    @classmethod
    def from_bytestring(cls, bytestring, include_identifier=True):
        """
        Create a Translation1d object from a compressed bytestring.

        Args:
            bytestring (bytes): The compressed bytestring.
            include_identifier (bool): Whether the bytestring includes the identifier. Defaults to True.

        Returns:
            Translation1d: A new Translation1d object with the magnitude from the bytestring.

        Raises:
            ValueError: If the bytestring is invalid.
        """
        if include_identifier:
            if not bytestring.startswith(TRANSLATION1D_IDENTIFIER):
                raise ValueError("Invalid bytestring for Translation1d, must start with " + str(TRANSLATION1D_IDENTIFIER.decode()))
            bytestring = bytestring[len(TRANSLATION1D_IDENTIFIER):]
        magnitude = float.fromhex(bytestring.decode())
        return cls(magnitude)


# Alias Translation1d as Distance
Distance = Translation1d
