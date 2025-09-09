import math
import struct

# Load polar coordinates from the binary file
polar_coordinates = []
with open("assets/calibration_coefficients.bin", "rb") as file:
    while chunk := file.read(8):  # Each record is 8 bytes (2 floats of 4 bytes each)
        r, theta = struct.unpack("ff", chunk)
        polar_coordinates.append((r, theta))

# Sort polar coordinates by theta
r_values = [point[0] for point in polar_coordinates]
theta_values = [point[1] for point in polar_coordinates]

print("Loaded {} polar coordinates from binary file.".format(len(polar_coordinates)))

def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta


def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def normalize_joystick_input(x, y):
    r, theta = cartesian_to_polar(x, y)

    # Find the two closest theta values
    for i in range(len(polar_coordinates) - 1):
        r_1, theta_1 = polar_coordinates[i]
        r_2, theta_2 = polar_coordinates[i + 1]

        if theta_1 <= theta <= theta_2:
            # Perform linear interpolation
            interpolated_r = r_1 + (r_2 - r_1) * (theta - theta_1) / (theta_2 - theta_1)
            break
    else:
        # If theta is out of bounds, return a default value or handle the edge case
        interpolated_r = polar_coordinates[-1][0]

    # Normalize the input using the interpolated radius
    scalar = interpolated_r
    normalized_x = x / scalar
    normalized_y = y / scalar

    return normalized_x, normalized_y
