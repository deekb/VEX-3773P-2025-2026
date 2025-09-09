import math
import struct

import matplotlib.pyplot as plt
import numpy as np

# Load polar coordinates from the binary file
polar_coordinates = []
with open("calibration_coefficients.bin", "rb") as file:
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


circle_points = [
    (math.cos(theta), math.sin(theta)) for theta in np.linspace(0, 2 * np.pi, 1000)
]

plt.figure(figsize=(12, 12))
plt.scatter(
    [point[0] for point in [normalize_joystick_input(x, y) for x, y in circle_points]],
    [point[1] for point in [normalize_joystick_input(x, y) for x, y in circle_points]],
    c="orange",
    label="Processed Data Points",
)
plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.title("Processed Coordinates Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()

# Plot polar coordinates and polynomial fit
plt.figure(figsize=(12, 6))
plt.scatter(theta_values, r_values, c="green", label="Calibration Coefficients graph")
plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.title("Polar Coordinates with Polynomial Fit")
plt.xlabel("Theta (radians)")
plt.ylabel("Radius")
plt.legend()
plt.show()
