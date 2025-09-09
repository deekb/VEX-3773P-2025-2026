import math
import struct

# Plot the points in Cartesian coordinates
x_values = eval(open("controller_x.txt").read())
y_values = eval(open("controller_y.txt").read())
points = list(zip(x_values, y_values))

# remove all points that are too close to the origin
points = [(x, y) for x, y in points if math.sqrt(x**2 + y**2) > 0.5]


def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta


polar_coordinates = [cartesian_to_polar(x, y) for x, y in points]
polar_coordinates = sorted(
    polar_coordinates, key=lambda polar: polar[1]
)  # Sort by theta


# Save the polar coordinates to a binary file
with open("calibration_coefficients.bin", "wb") as file:
    [file.write(struct.pack("ff", r, theta)) for r, theta in polar_coordinates]
