import math

import matplotlib.pyplot as plt
import numpy as np

# Plot the points in Cartesian coordinates
x_values = eval(open("controller_x.txt").read())
y_values = eval(open("controller_y.txt").read())
points = list(zip(x_values, y_values))

# remove all points that are too close to the origin
points = [(x, y) for x, y in points if math.sqrt(x**2 + y**2) > 0.1]

print(f"Loaded {len(points)} points")
print(points)

def cartesian_to_polar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return r, theta

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

polar_coordinates = [cartesian_to_polar(x, y) for x, y in points]
polar_coordinates = sorted(polar_coordinates, key=lambda polar: polar[1])  # Sort by theta
r_values = [point[0] for point in polar_coordinates]
theta_values = [point[1] for point in polar_coordinates]


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

half_points = [(point[0]/2, point[1]/2) for point in points]
circle_points = [(math.cos(theta)/2, math.sin(theta)/2) for theta in np.linspace(0, 2 * np.pi, 100)]

plt.figure(figsize=(12, 12))
plt.scatter([point[0] for point in points], [point[1] for point in points], c='blue', label='Data Points')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.title("Cartesian Coordinates Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()

plt.figure(figsize=(12, 12))
plt.scatter([point[0] for point in [normalize_joystick_input(x, y) for x, y in half_points]], [point[1] for point in [normalize_joystick_input(x, y) for x, y in half_points]], c='red', label='Processed Data Points')
plt.scatter([point[0] for point in [normalize_joystick_input(x, y) for x, y in circle_points]], [point[1] for point in [normalize_joystick_input(x, y) for x, y in circle_points]], c='orange', label='Processed Data Points')
plt.scatter([point[0] for point in [normalize_joystick_input(x, y) for x, y in points]], [point[1] for point in [normalize_joystick_input(x, y) for x, y in points]], c='purple', label='Processed Data Points')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.title("Processed Coordinates Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()


# Plot polar coordinates and polynomial fit
plt.figure(figsize=(12, 6))
plt.scatter(theta_values, r_values, c='green', label='Data Points')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.title("Polar Coordinates with Polynomial Fit")
plt.xlabel("Theta (radians)")
plt.ylabel("Radius")
plt.legend()
plt.ylim([1, 1.3])
plt.show()
