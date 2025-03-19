# GeometryUtil Class

This module provides various functions for calculating distances, areas, centroids, and other geometric properties. It also includes functions for handling lines and polygons.

## Functions

## `distance(point1, point2)`
Calculate the Euclidean distance between two points.

**Args:**
- `point1 (tuple)`: Coordinates of the first point (x1, y1).
- `point2 (tuple)`: Coordinates of the second point (x2, y2).

**Returns:**
- `float`: The Euclidean distance between the two points.

**Usage:**
Useful for determining the straight-line distance between two points in a 2D space.

## `area_triangle(point1, point2, point3)`
Calculate the area of a triangle formed by three points using Heron's formula.

**Args:**
- `point1 (tuple)`: Coordinates of the first point (x1, y1).
- `point2 (tuple)`: Coordinates of the second point (x2, y2).
- `point3 (tuple)`: Coordinates of the third point (x3, y3).

**Returns:**
- `float`: The area of the triangle.

**Usage:**
Useful for calculating the area of a triangle when the coordinates of its vertices are known.

## `centroid(points)`
Calculate the centroid (center of mass) of a list of points.

**Args:**
- `points (list)`: List of point coordinates [(x1, y1), (x2, y2), ...].

**Returns:**
- `tuple[float, float]`: Coordinates of the centroid (x, y).

**Usage:**
Useful for finding the geometric center of a set of points, often used in polygon calculations.

## `intersection_point(line1_start, line1_end, line2_start, line2_end)`
Calculate the intersection point of two lines defined by their endpoints.

**Args:**
- `line1_start (tuple)`: Starting point of the first line (x1, y1).
- `line1_end (tuple)`: Ending point of the first line (x2, y2).
- `line2_start (tuple)`: Starting point of the second line (x3, y3).
- `line2_end (tuple)`: Ending point of the second line (x4, y4).

**Returns:**
- `tuple or None`: Coordinates of the intersection point (x, y) if it exists, None otherwise.

**Usage:**
Useful for determining where two lines intersect, if at all.

## `is_point_inside_polygon(point, polygon)`
Check if a point is inside a polygon.

**Args:**
- `point (tuple)`: Coordinates of the point (x, y).
- `polygon (list)`: List of polygon vertices [(x1, y1), (x2, y2), ...].

**Returns:**
- `bool`: True if the point is inside the polygon, False otherwise.

**Usage:**
Useful for point-in-polygon tests, often used in graphical applications and geographic information systems (GIS).

## `polygon_area(polygon)`
Calculate the area of a polygon defined by its vertices using the shoelace formula.

**Args:**
- `polygon (list)`: List of polygon vertices [(x1, y1), (x2, y2), ...].

**Returns:**
- `float`: The area of the polygon.

**Usage:**
Useful for calculating the area of any polygon when the coordinates of its vertices are known.

## `circle_area(radius)`
Calculate the area of a circle given its radius.

**Args:**
- `radius (float)`: The radius of the circle.

**Returns:**
- `float`: The area of the circle.

**Usage:**
Useful for calculating the area of a circle when the radius is known.

## `circle_circumference(radius)`
Calculate the circumference of a circle given its radius.

**Args:**
- `radius (float)`: The radius of the circle.

**Returns:**
- `float`: The circumference of the circle.

**Usage:**
Useful for calculating the circumference of a circle, for example a wheel, when the radius is known.

## `rectangle_area(width, height)`
Calculate the area of a rectangle given its width and height.

**Args:**
- `width (float)`: The width of the rectangle.
- `height (float)`: The height of the rectangle.

**Returns:**
- `float`: The area of the rectangle.

**Usage:**
Useful for calculating the area of a rectangle when the width and height are known.

## `rectangle_perimeter(width, height)`
Calculate the perimeter of a rectangle given its width and height.

**Args:**
- `width (float)`: The width of the rectangle.
- `height (float)`: The height of the rectangle.

**Returns:**
- `float`: The perimeter of the rectangle.

**Usage:**
Useful for calculating the perimeter of a rectangle when the width and height are known.

## `closest_point_on_line(point, line_start, line_end)`
Find the closest point on a line to a given point.

**Args:**
- `point (tuple)`: Coordinates of the point (x, y).
- `line_start (tuple)`: Starting point of the line (x1, y1).
- `line_end (tuple)`: Ending point of the line (x2, y2).

**Returns:**
- `tuple`: Coordinates of the closest point on the line (x', y').

**Usage:**
Useful for finding the nearest point on a line segment to a given point.

## `arc_length_from_rotation(circle_circumference, rotation)`
Calculate the arc length traveled by a circle given its circumference and a rotation value.

**Args:**
- `circle_circumference (Distance)`: The circumference of the circle.
- `rotation`: The rotation value (in revolutions).

**Returns:**
- `float`: The arc length traveled by the circle.

**Usage:**
Useful in odometry for calculating the distance traveled by a wheel given its circumference and its change in rotation.