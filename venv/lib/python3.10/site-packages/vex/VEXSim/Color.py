from vex.VEXSim import vexnumber


class Color:
    """Color class - create a new color

    This class is used to create instances of color objects

    Args:
        value: The color value, can be specified in various ways, see examples.

    Returns:
        An instance of the Color class

    Examples:
        # create blue using hex value
        >>> c = Color(0x0000ff)
        # create blue using r, g, b values
        >>>c = Color(0, 0, 255)
        # create blue using web string
        >>>c = Color("#00F")
        # create blue using web string (alternate)
        >>>c = Color("#0000FF")
        # create red using an existing object
        >>>c = Color(Color.RED)
    """
    class DefinedColor:
        def __init__(self, value):
            self.value = value

    BLACK = DefinedColor(0x000000)
    """predefined Color black"""
    WHITE = DefinedColor(0xFFFFFF)
    """predefined Color white"""
    RED = DefinedColor(0xFF0000)
    """predefined Color red"""
    GREEN = DefinedColor(0x00FF00)
    """predefined Color green"""
    BLUE = DefinedColor(0x0000FF)
    """predefined Color blue"""
    YELLOW = DefinedColor(0xFFFF00)
    """predefined Color yellow"""
    ORANGE = DefinedColor(0xffa500)
    """predefined Color orange"""
    PURPLE = DefinedColor(0xff00ff)
    """predefined Color purple"""
    CYAN = DefinedColor(0x00ffff)
    """predefined Color cyan"""
    TRANSPARENT = DefinedColor(0x000000)
    """predefined Color transparent"""

    def __init__(self, *args):
        pass

    def rgb(self, *args):
        """### change existing Color instance to new rgb value

        #### Arguments:
            value : The color value, can be specified in various ways, see examples.

        #### Returns:
            integer value representing the color

        #### Examples:
            # create a color that is red
            c = Color(0xFF0000)
            # change color to blue using single value
            c.rgb(0x0000FF)
            # change color to green using three values
            c.rgb(0, 255, 0)
        """
        return 0

    def hsv(self, hue: vexnumber, saturation: vexnumber, value: vexnumber):
        """### change existing Color instance using hsv

        #### Arguments:
            hue : The hue of the color
            saturation : The saturation of the color
            value : The brightness of the color

        #### Returns:
            integer value representing the color

        #### Examples:
            # create a color that is red
            c.hsv( 0, 1.0, 1.0)
        """
        return 0

    def web(self, value: str):
        """### change existing Color instance using web string

        #### Arguments:
            value : The new color as a web string

        #### Returns:
            integer value representing the color

        #### Examples:
            # create a color that is red
            c.web("#F00")
        """
        return 0

    def is_transparent(self):
        """### return whether color is transparent or not

        #### Arguments:
            None

        #### Returns:
            True or False

        #### Examples:
        """
        return False
