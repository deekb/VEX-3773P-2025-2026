from math import pi


def range_reduction(x):
    # Step 1: Range reduction to [-pi, pi]
    return ((x + pi) % (2 * pi)) - pi


def approximate_sin(x):
    # x = range_reduction(x)

    # # Step 2: Further reduce to [-pi/2, pi/2] using sine properties
    # if x > pi / 2:
    #     x = pi - x  # Mirror in the second quadrant
    # elif x < -pi / 2:
    #     x = -pi - x  # Mirror in the third quadrant

    # Polynomial approximation for reduced x
    x1 = x / (2 * pi)
    x2 = x1 ** 2
    return x1 * (6.28317940663383263695539184084148414 + x2 * (-41.3389424984438475211600845004648977 + x2 * (
            81.3953586300215790478948871165643136 - 71.4746942820704835483055527883527435 * x2)))


def approximate_cos(x):
    """
    Approximate cosine using the sine approximation.
    cos(x) is computed as sin(pi/2 - x).
    """

    x = range_reduction(x)

    # Step 2: Use the shifted sine relationship
    shifted_x = pi / 2 - x

    # Use the existing sine approximation function
    return approximate_sin(shifted_x)


def approximate_tan(x):
    """
    Approximate cosine using the sine approximation.
    cos(x) is computed as sin(pi/2 - x).
    """

    # Use the existing sine approximation function
    return approximate_sin(x) / approximate_cos(x)

