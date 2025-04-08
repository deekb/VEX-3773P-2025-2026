from VEXLib.Geometry.Constants import TRANSLATION2D_IDENTIFIER, SEPERATOR
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation1d import Translation1d, Distance
import VEXLib.Geometry.GeometryUtil as GeometryUtil


class Translation2d:
    """Represents a 2D translation."""

    def __init__(self, translation_x=Translation1d(), translation_y=Translation1d()):
        """Initialize the Translation2d object with x and y coordinates.

        **Do not instantiate this class directly unless you are creating it with two Translation1d (aliased "Distance") objects,
        use the from_meters, from_centimeters, from_inches, or from_feet class methods**

        Args:
            translation_x (Translation1d): The x translation. Defaults to 0 meters.
            translation_y (Translation1d): The y translation. Defaults to 0 meters.
        """
        assert isinstance(translation_x, Translation1d), "To instantiate this class directly you must pass it two Translation1d (Distance) objects, if you wanted to create a new Translation2d from x, y coordinates as floats please use the  from_meters, from_centimeters, from_inches, or from_feet class methods"
        assert isinstance(translation_y, Translation1d), "To instantiate this class directly you must pass it two Translation1d (Distance) objects, if you wanted to create a new Translation2d from x, y coordinates as floats please use the  from_meters, from_centimeters, from_inches, or from_feet class methods"
        self.x_component = translation_x
        self.y_component = translation_y

    def __add__(self, other):
        """Add two Translation2d objects.

        Args:
            other (Translation2d): The other Translation2d object to add.

        Returns:
            Translation2d: A new Translation2d object with the summed coordinates.
        """
        return Translation2d(self.x_component + other.x_component, self.y_component + other.y_component)

    def __radd__(self, other):
        """Add two Translation2d objects."""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtract two Translation2d objects.

        Args:
            other (Translation2d): The other Translation2d object to subtract.

        Returns:
            Translation2d: A new Translation2d object with the subtracted coordinates.
        """
        return Translation2d(self.x_component - other.x_component, self.y_component - other.y_component)

    def __rsub__(self, other):
        """Reverse subtract two Translation2d objects."""
        return Translation2d(other.x_component - self.x_component, other.y_component - self.y_component)

    def __mul__(self, scalar):
        """Multiply Translation2d by a scalar.

        Args:
            scalar (float): The scalar to multiply with.

        Returns:
            Translation2d: A new Translation2d object with the scaled coordinates.
        """
        return Translation2d(self.x_component * scalar, self.y_component * scalar)

    def __rmul__(self, scalar):
        """Reverse multiply Translation2d by a scalar."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """Divide Translation2d by a scalar.

        Args:
            scalar (float): The scalar to divide with.

        Returns:
            Translation2d: A new Translation2d object with the scaled coordinates.
        """
        return Translation2d(self.x_component / scalar, self.y_component / scalar)

    def __rtruediv__(self, scalar):
        """Reverse divide Translation2d by a scalar."""
        return Translation2d(scalar / self.x_component, scalar / self.y_component)

    def __eq__(self, other):
        """Check if two Translation2d objects are equal.

        Args:
            other (Translation2d): The other Translation2d object to compare.

        Returns:
            bool: True if the x and y coordinates are equal, False otherwise.
        """
        return self.x_component == other.x_component and self.y_component == other.y_component

    def __str__(self):
        """Return the string representation of Translation2d.

        Returns:
            str: The string representation of the x and y coordinates.
        """
        return "(" + str(self.x_component) + ", " + str(self.y_component) + ")"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_polar(cls, distance: Translation1d, angle: Rotation2d):
        """
        Construct a Translation2d object from a set of polar coordinates, (a translation and rotation)

        Args:
            distance: A Translation1d object representing the distance.
            angle: A Rotation2d object representing the rotation.

        Returns:

        """
        if not isinstance(distance, Translation1d):
            raise ValueError("Distance must be a Translation1d object")
        elif not isinstance(angle, Rotation2d):
            raise ValueError("Angle must be a Rotation2d object")

        return cls(translation_x=distance * angle.cos(),
                   translation_y=distance * angle.sin())

    @classmethod
    def from_meters(cls, x_meters, y_meters):
        """Create a Translation2d object from meters.

        Args:
            x_meters (float): The x coordinate in meters.
            y_meters (float): The y coordinate in meters.

        Returns:
            Translation2d: A new Translation2d object with the x and y coordinates in meters.
        """
        return cls(Translation1d.from_meters(x_meters), Translation1d.from_meters(y_meters))

    @classmethod
    def from_centimeters(cls, x_centimeters, y_centimeters):
        """Create a Translation2d object from centimeters.

        Args:
            x_centimeters (float): The x coordinate in centimeters.
            y_centimeters (float): The y coordinate in centimeters.

        Returns:
            Translation2d: A new Translation2d object with the x and y coordinates converted to meters.
        """
        return cls(Translation1d.from_centimeters(x_centimeters), Translation1d.from_centimeters(y_centimeters))

    @classmethod
    def from_inches(cls, x_inches, y_inches):
        """Create a Translation2d object from inches.

        Args:
            x_inches (float): The x coordinate in inches.
            y_inches (float): The y coordinate in inches.

        Returns:
            Translation2d: A new Translation2d object with the x and y coordinates converted to meters.
        """
        return cls(Translation1d.from_inches(x_inches), Translation1d.from_inches(y_inches))

    @classmethod
    def from_feet(cls, x_feet, y_feet):
        """Create a Translation2d object from feet.

        Args:
            x_feet (float): The x coordinate in feet.
            y_feet (float): The y coordinate in feet.

        Returns:
            Translation2d: A new Translation2d object with the x and y coordinates converted to meters.
        """
        return cls(Translation1d.from_feet(x_feet), Translation1d.from_feet(y_feet))

    def to_meters(self):
        """Convert the x and y coordinates to meters.

        Returns:
            tuple[float, float]: A tuple containing the x and y coordinates in meters.
        """
        return self.x_component.to_meters(), self.y_component.to_meters()

    def to_centimeters(self):
        """Convert the x and y coordinates to centimeters.

        Returns:
            tuple[float, float]: A tuple containing the x and y coordinates in centimeters.
        """
        return self.x_component.to_centimeters(), self.y_component.to_centimeters()

    def to_inches(self):
        """Convert the x and y coordinates to inches.

        Returns:
            tuple[float, float]: A tuple containing the x and y coordinates in inches.
        """
        return self.x_component.to_inches(), self.y_component.to_inches()

    def distance(self, other):
        """Calculate the cartesian distance between this and another translation.

        Args:
            other (Translation2d): The other translation.

        Returns:
            Distance: The distance between the two translation.
        """
        return Distance.from_meters(GeometryUtil.distance(self.to_meters(), other.to_meters()))

    def length(self):
        """Calculate the cartesian distance between this translation and the origin.

        Returns:
            Length: The distance from the origin to the translation.
        """
        return Distance.from_meters(GeometryUtil.distance(self.to_meters(), (0, 0)))

    def rotate_by(self, rotation2d):
        sin_other = rotation2d.sin()
        cos_other = rotation2d.cos()

        new_x = self.x_component.to_meters() * cos_other - self.y_component.to_meters() * sin_other
        new_y = self.x_component.to_meters() * sin_other + self.y_component.to_meters() * cos_other

        return Translation2d(Translation1d.from_meters(new_x), Translation1d.from_meters(new_y))

    def inverse(self):
        """
        Calculates the unary inverse of a translation2d object, equivalent to rotating it by a half-turn
        Returns:
            A rotation2d object that is the original translation rotated by a half-turn

        """
        return self.rotate_by(Rotation2d.from_revolutions(0.5))

    def angle(self):
        """
        Returns the angle (positive counterclockwise) that this translation forms with the positive X axis.

        Returns:
            The angle of the translation
        """

        return Rotation2d.from_translation2d(self)

    def to_bytestring(self, include_identifier=True):
        """Return a compressed bytestring representing the Velocity2d in meters per second."""
        x_bytes = self.x_component.to_bytestring(include_identifier=False)
        y_bytes = self.y_component.to_bytestring(include_identifier=False)
        return (TRANSLATION2D_IDENTIFIER if include_identifier else b"") + x_bytes + SEPERATOR + y_bytes

    @classmethod
    def from_bytestring(cls, bytestring):
        """Create a Velocity2d object from a compressed bytestring."""
        if not bytestring.startswith(TRANSLATION2D_IDENTIFIER):
            raise ValueError("Invalid bytestring for Translation2d, must start with " + str(TRANSLATION2D_IDENTIFIER))
        x_str, y_str = bytestring[len(TRANSLATION2D_IDENTIFIER):].split(SEPERATOR)
        x_magnitude = Translation1d.from_bytestring(x_str, include_identifier=False)
        y_magnitude = Translation1d.from_bytestring(y_str, include_identifier=False)
        return cls(x_magnitude, y_magnitude)