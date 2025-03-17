"""
MathUtil Module
Provides a set of utility functions to perform various mathematical operations such as interpolation, wrapping values,
calculating angular differences, and applying filters. These functions are designed to assist in mathematical calculations
relevant to robotics, geometry, and numerical computation.
"""
import math

from VEXLib.Geometry.GeometryUtil import hypotenuse


def sign(x: float) -> float:
    """
    Determine the sign of a number.

    Args:
        x (float): The input number.

    Returns:
        float: 1 for positive or zero, -1 for negative.

    Examples:
        >>> sign(10.0)
        1
        >>> sign(-5.0)
        -1
        >>> sign(0.0)
        1
    """
    return 1 if x >= 0 else -1


def average(*args: float) -> float:
    """
    Calculates the average of the input arguments.

    Args:
        *args: The values to average (int | float).

    Returns:
        The average of all the values.

    Examples:
        >>> average(1.0, 2.0, 3.0)
        2.0
        >>> average(5.0, 10.0)
        7.5
        >>> average(3.5, 4.5, 6.0)
        4.666666666666667
        >>> average(1.0, 2.0, 3.0, 4.0, 5.0)
        3.0
    """
    return average_iterable(list(args))


def average_iterable(iterable: list[float]) -> float:
    """
    Calculates the average of the input iterable.

    Args:
        iterable: The list of values to average iterable[(int | float)].

    Returns:
        The average of all the values in the iterable.

    Examples:
        >>> average_iterable([1.0, 2.0, 3.0])
        2.0
        >>> average_iterable([5.0, 10.0])
        7.5
        >>> average_iterable([3.5, 4.5, 6.0])
        4.666666666666667
        >>> average_iterable([1.0, 2.0, 3.0, 4.0, 5.0])
        3.0
    """
    return sum(iterable) / len(iterable)


def clamp(value: float, lower_limit: float | None = None, upper_limit: float | None = None) -> float:
    """
    Restricts a value within a specified range.

    Args:
        value: The value to be clamped.
        lower_limit: The lower limit of the range. If None is specified, no lower limit is applied.
        upper_limit: The upper limit of the range. If None is specified, no upper limit is applied.

    Returns:
        The clamped value.

    Examples:
        >>> clamp(5.0, 1.0, 10.0)
        5.0
        >>> clamp(0.0, 1.0, 10.0)
        1.0
        >>> clamp(15.0, 1.0, 10.0)
        10.0
        >>> clamp(5.0, None, 10.0)
        5.0
        >>> clamp(5.0, 1.0, None)
        5.0
    """
    if lower_limit is not None and upper_limit is not None and upper_limit < lower_limit:
        raise ValueError(
            "The value of upper_limit should be greater than or equal to that of lower_limit"
        )

    if lower_limit is not None:
        if value < lower_limit:
            return lower_limit
    if upper_limit is not None:
        if value > upper_limit:
            return upper_limit
    return value


def apply_deadband(value: float, deadband: float = 0.05, max_magnitude: float = 1.0) -> float:
    """
    Returns 0.0 if the given value is within the specified range around zero. The remaining range
    between the deadband and the maximum magnitude is scaled from 0.0 to the maximum magnitude.

    Args:
        value: The value to clip.
        deadband: The range around zero.
        max_magnitude: The maximum magnitude of the input.

    Returns:
        The value after the deadband is applied.

    Examples:
        >>> apply_deadband(0.03)
        0.0
        >>> apply_deadband(0.1)
        0.052631578947368425
        >>> apply_deadband(-0.1)
        -0.052631578947368425
        >>> apply_deadband(0.1, 0.1)
        0.0
    """
    if abs(value) > max_magnitude:
        raise ValueError

    if abs(value) <= deadband:
        return 0.0

    return sign(value) * max_magnitude * (abs(value) - deadband) / (max_magnitude - deadband)


def input_modulus(input_: float, minimum_input: float, maximum_input: float) -> float:
    """
    Wraps an input value into a specified range.

    Args:
        input_ (float): The value to wrap.
        minimum_input (float): The minimum value of the range.
        maximum_input (float): The maximum value of the range.

    Returns:
        float: The wrapped value within the range minimum_input, maximum_input inclusive of maximum_input but exclusive of minimum_input.

    Examples:
        >>> input_modulus(370.0, 0.0, 360.0)
        10.0
        >>> input_modulus(-10.0, 0.0, 360.0)
        350.0
        >>> input_modulus(370.0, -180.0, 180.0)
        10.0
        >>> input_modulus(-190.0, -180.0, 180.0)
        170.0
    """
    modulus = maximum_input - minimum_input
    if modulus <= 0:
        raise ValueError("Maximum input must be greater than minimum input")

    wrapped_value = (input_ - minimum_input) % modulus
    if wrapped_value < 0:
        wrapped_value += modulus

    return wrapped_value + minimum_input


def angle_modulus(angle_radians: float) -> float:
    """
    Wraps an angle to the range > -pi and <= pi radians.

    Args:
        angle_radians: Angle to wrap in radians.

    Returns:
        The wrapped angle.

    Examples:
        >>> angle_modulus(3 * math.pi)
        3.141592653589793
        >>> angle_modulus(-3 * math.pi)
        3.141592653589793
        >>> angle_modulus(math.pi)
        3.141592653589793
        >>> angle_modulus(-math.pi)
        3.141592653589793
    """
    angle = input_modulus(angle_radians, -math.pi, math.pi)
    if angle == -math.pi:
        return math.pi
    return angle


def interpolate(start_value: float, end_value: float, t: float, allow_extrapolation: bool = True) -> float:
    """
    Perform linear interpolation between two values.

    Args:
        start_value: The value to start at.
        end_value: The value to end at.
        t: How far between the two values to interpolate. With zero corresponding to start_value and 1 corresponding to end_value. Unless the allow_extrapolation flag is set This is clamped to the range [0, 1].
        allow_extrapolation: Whether to allow the output value to go beyond the bounds of start_value and end_value

    Returns:
        The interpolated value.

    Examples:
        >>> interpolate(0.0, 10.0, 0.5)
        5.0
        >>> interpolate(0.0, 10.0, 1.5)
        15.0
        >>> interpolate(0.0, 10.0, 1.5, allow_extrapolation=False)
        10.0
        >>> interpolate(0.0, 10.0, -0.5, allow_extrapolation=False)
        0.0
    """
    if not allow_extrapolation:
        t = clamp(t, 0, 1)

    return start_value + (end_value - start_value) * t


def interpolate_2d(x1: float, x2: float, y1: float, y2: float, x: float, allow_extrapolation: bool = True) -> float:
    """
    Perform linear interpolation for x between (x1,y1) and (x2,y2)

    Args:
        x1: The first point's X value
        x2: The first point's Y value
        y1: The second point's X value
        y2: The second point's Y value
        x: The x value to interpolate the Y value for
        allow_extrapolation (bool): Whether to allow the output value to go beyond the bounds of (x1, y1) and (x2, y2).

    Returns:
        The Y value for the given x value, calculated using linear interpolation from the points given

    Examples:
        >>> interpolate_2d(0.0, 10.0, 0.0, 20.0, 5.0)
        10.0
        >>> interpolate_2d(0.0, 10.0, 0.0, 20.0, 15.0)
        30.0
        >>> interpolate_2d(0.0, 10.0, 0.0, 20.0, 15.0, allow_extrapolation=False)
        20.0
        >>> interpolate_2d(0.0, 10.0, 0.0, 20.0, -5.0, allow_extrapolation=False)
        0.0
    """
    if not allow_extrapolation:
        if x < x1:
            return y1
        elif x > x2:
            return y2

    return ((y2 - y1) * x + x2 * y1 - x1 * y2) / (x2 - x1)


def inverse_interpolate(start_value: float, end_value: float, q: float, allow_extrapolation: bool = True) -> float:
    """
    Return where within interpolation range [0, 1] q is between start_value and end_value.

    Args:
        start_value (float): Lower part of interpolation range.
        end_value (float): Upper part of interpolation range.
        q (float): Query.
        allow_extrapolation (bool): Whether to allow the output value to go beyond the bounds of start_value and end_value.

    Returns:
        float: Interpolant in range [0, 1].

    Examples:
        >>> inverse_interpolate(0.0, 10.0, 5.0)
        0.5
        >>> inverse_interpolate(0.0, 10.0, 15.0)
        1.5
        >>> inverse_interpolate(0.0, 10.0, 15.0, allow_extrapolation=False)
        1.0
        >>> inverse_interpolate(0.0, 10.0, -5.0, allow_extrapolation=False)
        0.0
    """
    total_range = end_value - start_value
    if total_range <= 0:
        return 0.0

    query_to_start = q - start_value
    if query_to_start <= 0:
        return 0.0

    interpolant = query_to_start / total_range
    if not allow_extrapolation:
        return clamp(interpolant, 0.0, 1.0)
    return interpolant


def is_near(expected, actual, tolerance) -> bool:
    """
    Checks if the given value matches an expected value within a certain tolerance.

    Args:
        expected (float): The expected value.
        actual (float): The actual value.
        tolerance (float): The allowed difference between the actual and the expected value.

    Returns:
        bool: Whether the actual value is within the allowed tolerance.

    Examples:
        >>> is_near(10.0, 10.1, 0.2)
        True
        >>> is_near(10.0, 10.3, 0.2)
        False
        >>> is_near(10.0, 9.9, 0.2)
        True
        >>> is_near(10.0, 9.7, 0.2)
        False
    """
    if tolerance < 0:
        raise ValueError("Tolerance must be a non-negative number!")

    return abs(expected - actual) < tolerance


def is_near_continuous(expected, actual, tolerance, minimum, maximum):
    """
    Checks if the given value matches an expected value within a certain tolerance. Supports
    continuous input for cases like absolute encoders.

    Continuous input means that the min and max value are considered to be the same point, and
    tolerances can be checked across them. A common example would be for absolute encoders: calling
    is_near_continuous(2.0, 359.0, 5.0, 0.0, 360.0) returns true because 359.0 is 1.0 away from 360.0 (which is treated as the
    same as 0.0) and 2.0 is 2.0 away from 0.0, adding up to an error of 3.0 degrees, which is within the
    given tolerance of 5.0.

    Args:
        expected (float): The expected value.
        actual (float): The actual value.
        tolerance (float): The allowed difference between the actual and the expected value.
        minimum (float): Smallest value before wrapping around to the largest value.
        maximum (float): Largest value before wrapping around to the smallest value.

    Returns:
        bool: Whether the actual value is within the allowed tolerance.

    Examples:
        >>> is_near_continuous(2.0, 359.0, 5.0, 0.0, 360.0)
        True
        >>> is_near_continuous(2.0, 355.0, 5.0, 0.0, 360.0)
        False
        >>> is_near_continuous(2.0, 3.0, 5.0, 0.0, 360.0)
        True
        >>> is_near_continuous(2.0, 8.0, 5.0, 0.0, 360.0)
        False
    """
    if tolerance < 0:
        raise ValueError("Tolerance must be non-negative!")

    # Max error is exactly halfway between the min and max
    error_bound = (maximum - minimum) / 2.0
    error = input_modulus(expected - actual, -error_bound, error_bound)
    return abs(error) < tolerance


def distance_continuous(expected, actual, minimum, maximum):
    """
    Checks if the given value matches an expected value within a certain tolerance. Supports
    continuous input for cases like absolute encoders.

    Continuous input means that the min and max value are considered to be the same point, and
    tolerances can be checked across them. A common example would be for absolute encoders: calling
    is_near_continuous(2.0, 359.0, 5.0, 0.0, 360.0) returns true because 359.0 is 1.0 away from 360.0 (which is treated as the
    same as 0.0) and 2.0 is 2.0 away from 0.0, adding up to an error of 3.0 degrees, which is within the
    given tolerance of 5.0.

    Args:
        expected (float): The expected value.
        actual (float): The actual value.
        minimum (float): Smallest value before wrapping around to the largest value.
        maximum (float): Largest value before wrapping around to the smallest value.

    Returns:
        float: The smallest distance between the actual and the expected.

    Examples:
        >>> distance_continuous(2.0, 359.0, 0.0, 360.0)
        3.0
        >>> distance_continuous(2.0, 355.0, 0.0, 360.0)
        7.0
        >>> distance_continuous(2.0, 3.0, 0.0, 360.0)
        1.0
        >>> distance_continuous(2.0, 8.0, 0.0, 360.0)
        6.0
    """
    # Max error is exactly halfway between the min and max
    error_bound = (maximum - minimum) / 2.0
    error = input_modulus(expected - actual, -error_bound, error_bound)
    return abs(error)


def cubic_filter(value, linearity=0.0) -> float:
    """
    Apply a cubic filter to a value with a given linearity

    Args:
        value: The value between -1 to 1 to apply the filter to
        linearity: How linear to make the filter (0 for fully cubic, 1 for fully linear)

    Returns:
        The input value with a cubic filter applied

    Examples:
        >>> cubic_filter(0.5)
        0.125
        >>> cubic_filter(0.5, 1.0)
        0.5
        >>> cubic_filter(-0.5)
        -0.125
        >>> cubic_filter(-0.5, 1.0)
        -0.5
    """
    if abs(value) > 1:
        raise ValueError("Input value must be between -1 and 1")
    if linearity < 0 or linearity > 1:
        raise ValueError("Linearity must be between 0 and 1 (inclusive))")

    return ((value ** 3) * (1 - linearity)) + value * linearity


def slope_intercept_to_standard(slope, intercept):
    """
    Convert a linear equation from slope-intercept form to standard form.

    Args:
        slope (float): The slope of the line.
        intercept (float): The y-intercept of the line.

    Returns:
        tuple: Coefficients (A, B, C) of the line equation in standard form Ax + By + C = 0.

    Examples:
        >>> slope_intercept_to_standard(2, 3)
        (2, -1, 3)
        >>> slope_intercept_to_standard(-2, 3)
        (2, 1, -3)
        >>> slope_intercept_to_standard(0, 3)
        (0, -1, 3)
        >>> slope_intercept_to_standard(2, 0)
        (2, -1, 0)
    """
    # Step 1: Move terms to one side
    # y = mx + b --> mx - y + b = 0
    a = slope
    b = -1
    c = intercept

    # Step 2: Ensure positive coefficient of x
    # If the coefficient of x is negative, multiply both sides by -1
    if a < 0:
        a *= -1
        b *= -1
        c *= -1

    return a, b, c


def standard_to_x_intercept(a, b, c):
    """
    Calculate the x-intercept of a line from its equation in standard form.

    Args:
        a (float): Coefficient of x in the standard form equation Ax + By + C = 0.
        b (float): Coefficient of y in the standard form equation Ax + By + C = 0.
        c (float): Constant term in the standard form equation Ax + By + C = 0.

    Returns:
        float or None: The x-intercept of the line. Returns None if the line is vertical (B == 0).

    Examples:
        >>> standard_to_x_intercept(1, 2, 3)
        -3.0
        >>> standard_to_x_intercept(0, 2, 3)

        >>> standard_to_x_intercept(4, 5, 6)
        -1.5
        >>> standard_to_x_intercept(2, 0, 8)
        -4.0
    """
    if a == 0:
        return None
    x_intercept = -c / a
    return x_intercept


def distance_from_point_to_line(point, slope, y_intercept):
    """
    Calculate the distance from a point to a line.

    Args:
        point (tuple): The coordinates of the point (x0, y0).
        slope (float): The slope of the line. If slope is infinite, it represents a vertical line.
        y_intercept (float): The y-intercept of the line.

    Returns:
        float: The perpendicular distance from the point to the line.

    Examples:
        >>> distance_from_point_to_line((1, 2), 1, 0)
        0.7071067811865475
        >>> distance_from_point_to_line((1, 2), float('inf'), 0)
        1.0
        >>> distance_from_point_to_line((3, 4), 2, 1)
        1.3416407864998738
        >>> distance_from_point_to_line((5, 6), -1, 2)
        2.8284271247461903
    """
    x0, y0 = point
    a, b, c = slope_intercept_to_standard(slope, y_intercept)
    if math.isinf(slope):
        x_intercept = standard_to_x_intercept(a, b, c)
        return abs(x0 - x_intercept)
    else:
        distance = abs(a * x0 + b * y0 + c) / hypotenuse(a, b)
        return distance


def factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    Args:
        n (int): The non-negative integer to calculate the factorial of.

    Returns:
        int: The factorial of the input integer.

    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(3)
        6
        >>> factorial(7)
        5040
    """
    result = 1
    for i in range(n + 1):
        if i:
            result *= i
    return result


def smallest_angular_difference(current, target):
    """
    Calculate the shortest angular difference between the current and target headings.
    This will return a value such that if you add it to the current heading you will get a value that represents the
    shortest path to the target heading. This value will be in the range -π to π.

    Args:
        current (float): The current heading in radians.
        target (float): The target heading in radians.

    Returns:
        float: The signed angular difference between the current and target. The result is in the range (-π, π],
               inclusive of π and exclusive of -π.

    Examples:
        >>> smallest_angular_difference(math.pi, -math.pi)
        0.0
        >>> smallest_angular_difference(0, math.pi)
        3.141592653589793
        >>> smallest_angular_difference(math.pi / 2, -math.pi / 2)
        3.141592653589793
        >>> smallest_angular_difference(0, 3 * math.pi / 2)
        -1.5707963267948966
    """
    tau = 2 * math.pi
    current %= 2 * tau
    target %= tau
    angular_difference = target - current
    if angular_difference > math.pi:
        angular_difference -= tau
    elif angular_difference < -math.pi:
        angular_difference += tau
    return angular_difference
