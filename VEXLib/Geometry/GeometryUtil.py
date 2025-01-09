"""
Geometry Utility Module

This module provides utility functions to perform various geometric calculations efficiently.

It includes algorithms for:
- Basic distance calculations between points.
- Computation of areas (triangles, rectangles, circles, polygons).
- Finding centroids of polygons and closest points on lines.
- Line segment and polygon-based operations such as intersection checks.
- Calculating arc-lengths for circular rotations.

This module aims to simplify geometric computations while programming VEX robots

Module Contents:
- Distance utility functions
- Area calculations (circles, polygons, triangles, rectangles)
- Line and polygon intersection checks.
- Centroid and geometric property calculations.
- Circle-related properties like circumference and arc lengths.
"""

import math

from VEXLib.Geometry.Translation1d import Distance, Translation1d


def hypotenuse(x: float, y: float) -> float:
    """
    Compute the hypotenuse of a right triangle given its two side lengths.

    Args:
        x (float): The length of one leg of the triangle.
        y (float): The length of the other leg of the triangle.

    Returns:
        float: The length of the hypotenuse (longest side of the triangle).
    """

    return math.sqrt(pow(x, 2) + pow(y, 2))


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """
    Compute the Euclidean distance between two points in a 2D plane.

    Args:
        point1 (tuple[float, float]): Coordinates of the first point as (x1, y1).
        point2 (tuple[float, float]): Coordinates of the second point as (x2, y2).

    Returns:
        float: The straight-line distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def area_triangle(point1: tuple[float, float], point2: tuple[float, float], point3: tuple[float, float]) -> float:
    """
    Compute the area of a triangle defined by three points using Heron's formula.

    Args:
        point1 (tuple[float, float]): Coordinates of the first vertex of the triangle.
        point2 (tuple[float, float]): Coordinates of the second vertex of the triangle.
        point3 (tuple[float, float]): Coordinates of the third vertex of the triangle.

    Returns:
        float: The area enclosed by the triangle.
    """
    a = distance(point1, point2)
    b = distance(point2, point3)
    c = distance(point3, point1)
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def centroid(points: list[tuple[float, float]]) -> tuple[float, float]:
    """
    Calculate the centroid (center of mass) of a closed 2D polygon.

    Args:
        points (list[tuple[float, float]]): List of polygon vertices defined as [(x1, y1), (x2, y2), ...].

    Returns:
        tuple[float, float]: Coordinates of the centroid (x, y), the center of mass.
    """
    total_area = 0
    centroid_x = 0
    centroid_y = 0

    for i, point in enumerate(points):
        j = (i + 1) % len(points)
        factor = point[0] * points[j][1] - points[j][0] * point[1]
        total_area += factor
        centroid_x += (point[0] + points[j][0]) * factor
        centroid_y += (point[1] + points[j][1]) * factor

    total_area /= 2
    centroid_x /= (6 * total_area)
    centroid_y /= (6 * total_area)

    return centroid_x, centroid_y


def intersection_point(line1_start: tuple[float, float], line1_end: tuple[float, float],
                       line2_start: tuple[float, float], line2_end: tuple[float, float]) -> tuple[float, float] | None:
    """
    Determine the intersection point of two line segments, if it exists.

    Args:
        line1_start (tuple): Starting point of the first line (x1, y1).
        line1_end (tuple): Ending point of the first line (x2, y2).
        line2_start (tuple): Starting point of the second line (x3, y3).
        line2_end (tuple): Ending point of the second line (x4, y4).

    Returns:
        tuple or None: Coordinates of the intersection point (x, y) if it exists, None otherwise.
    """
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if det == 0:
        return None  # Lines are parallel

    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

    # Check if the intersection point is within the line segments
    if (min(x1, x2) <= intersection_x <= max(x1, x2) and
            min(y1, y2) <= intersection_y <= max(y1, y2) and
            min(x3, x4) <= intersection_x <= max(x3, x4) and
            min(y3, y4) <= intersection_y <= max(y3, y4)):
        return intersection_x, intersection_y
    return None


def is_point_inside_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    """
    Determines if a given point lies within a closed 2D polygon using the ray-casting algorithm.

    Args:
        point (tuple[float, float]): The coordinates of the point as (x, y).
        polygon (list[tuple[float, float]]): A list of vertices defining the polygon, each represented as (x, y).

    Returns:
        bool: True if the point is inside the polygon; otherwise, False.
    """
    num_vertices = len(polygon)  # Total number of vertices in the polygon.
    intersection_count = 0  # Count of ray-polygon edge intersections.

    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1]) and point[0] < (polygon[j][0] - polygon[i][0]) * (
                point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            intersection_count += 1

    return intersection_count % 2 == 1


def polygon_area(polygon: list[tuple[float, float]]) -> float:
    """
    Calculates the area of a polygon using the Shoelace formula.

    Args:
        polygon (list[tuple[float, float]]): List of ordered vertices defining the polygon, each represented as (x, y).

    Returns:
        float: The computed area of the polygon.
    """
    num_vertices = len(polygon)
    area = 0

    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        area += (polygon[i][0] * polygon[j][1]) - (polygon[j][0] * polygon[i][1])

    return abs(area) / 2


def circle_area(radius: float) -> float:
    """
    Calculates the area of a circle given its radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle, calculated as π × radius².
    """
    return math.pi * radius ** 2


def circle_circumference(radius: float | Distance) -> float | Distance:
    """
    Calculates the circumference of a circle given its radius.

    Args:
        radius (float | Distance): The radius of the circle, which can be a scalar (float) or a Distance object.

    Returns:
        float | Distance: The circumference, calculated as 2 × π × radius.
    """
    return radius * 2 * math.pi


def rectangle_area(width: float, height: float) -> float:
    """
    Calculates the area of a rectangle given its width and height.

    Args:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Returns:
        float: The computed area of the rectangle (width × height).
    """
    return width * height


def rectangle_perimeter(width: float, height: float) -> float:
    """
    Calculates the perimeter of a rectangle based on its width and height.

    Args:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Returns:
        float: The perimeter of the rectangle, calculated as 2 × (width + height).
    """
    return 2 * (width + height)


def closest_point_on_line(point: tuple[float, float], line_start: tuple[float, float], line_end: tuple[float, float]) -> \
        tuple[float, float]:
    """
    Finds the closest point on a line segment to a given point in 2D space.

    Args:
        point (tuple[float, float]): The point's coordinates (x, y).
        line_start (tuple[float, float]): The starting coordinates (x1, y1) of the line segment.
        line_end (tuple[float, float]): The ending coordinates (x2, y2) of the line segment.

    Returns:
        tuple[float, float]: The coordinates of the closest point on the line segment.
    """
    x1, y1 = line_start
    x2, y2 = line_end
    x0, y0 = point

    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return line_start  # Start and end are the same point

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))  # Clamp to segment

    x_closest = x1 + t * dx
    y_closest = y1 + t * dy

    return x_closest, y_closest


def arc_length_from_rotation(circle_circumference: Translation1d, rotation) -> Translation1d:
    """
    Calculate the arc length traveled by a circle given its circumference and a rotation value.

    Args:
        circle_circumference (Translation1d): The circumference of the circle.
        rotation: The rotation value (in revolutions).

    Returns:
        Translation1d: The arc length traveled by the circle.
    """
    return circle_circumference * rotation.to_revolutions()
