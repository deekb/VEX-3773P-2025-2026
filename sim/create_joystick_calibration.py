import math
import struct

import pandas as pd

from VEXLib.Geometry.GeometryUtil import distance

# # Plot the points in Cartesian coordinates
# x_values = eval(open("controller_x.txt").read())
# y_values = eval(open("controller_y.txt").read())

df = pd.read_csv("left_stick_values.csv")

# Ensure expected columns exist
expected_cols = ["x", "y"]
for col in expected_cols:
    if col not in df.columns:
        raise ValueError(f"Missing expected column in csv file: {col}")

x_values = df["x"]
y_values = df["y"]


points = list(zip(x_values, y_values))

# remove all points that are too close to the origin
points = [point for point in points if distance((0, 0), point) > 0.8]


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
