# Translation2d Class

Represents a 2D translation.

## Features

- **Create** a `Translation2d` object from meters, centimeters, inches, or feet using the `from_<unit>` class methods. This is the most explicit and least error-prone way to use the class.
- **Add** or **subtract** two `Translation2d` objects.
- **Multiply** a `Translation2d` object by a scalar.
- **Check equality** between two `Translation2d` objects.
- **Convert** the coordinates to meters, centimeters, or inches.
- **Calculate the distance** between two `Translation2d` objects.
- **Calculate the length** of a `Translation2d` object from the origin.
- **Rotate** a `Translation2d` object by a given angle.
- **Calculate the inverse** of a `Translation2d` object.
- **Calculate the angle** of a `Translation2d` object with the positive X axis.

## Examples

### Create a Translation2d object from different units

```python
from VEXLib.Geometry.Translation2d import Translation2d

translation_meters = Translation2d.from_meters(3, 4)
print(translation_meters)  # Output: (3m, 4m)

translation_centimeters = Translation2d.from_centimeters(300, 400)
print(translation_centimeters)  # Output: (3m, 4m)

translation_inches = Translation2d.from_inches(118.11, 157.48)
print(translation_inches)  # Output: (3m, 4m)

translation_feet = Translation2d.from_feet(9.84252, 13.1234)
print(translation_feet)  # Output: (3m, 4m)
```

### Add two Translation2d objects

```python
sum_translation = translation_meters + translation_centimeters
print(sum_translation)  # Output: (6m, 8m)
```

### Subtract two Translation2d objects

```python
difference_translation = translation_meters - translation_centimeters
print(difference_translation)  # Output: (0m, 0m)
```

### Multiply a Translation2d object by a scalar

```python
scaled_translation = translation_meters * 2
print(scaled_translation)  # Output: (6m, 8m)
```

### Check equality between two Translation2d objects

```python
are_equal = translation_meters == translation_centimeters
print(are_equal)  # Output: True
```

### Convert the coordinates to different units

```python
print(translation_meters.to_centimeters())  # Output: (300.0, 400.0)
print(translation_meters.to_inches())       # Output: (118.11023622047244, 157.48031496062992)
```

### Calculate the distance between two Translation2d objects

```python
distance = translation_meters.distance(translation_centimeters)
print(distance)  # Output: 0m
```

### Calculate the length of a Translation2d object from the origin

```python
length = translation_meters.length()
print(length)  # Output: 5m
```

### Rotate a Translation2d object by a given angle

```python
from VEXLib.Geometry.Rotation2d import Rotation2d

rotation = Rotation2d.from_degrees(90)
rotated_translation = translation_meters.rotate_by(rotation)
print(rotated_translation)  # Output: (-4m, 3m)
```

### Calculate the inverse of a Translation2d object

```python
inverse_translation = translation_meters.inverse()
print(inverse_translation)  # Output: (-3m, -4m)
```

### Calculate the angle of a Translation2d object with the positive X axis

```python
angle = translation_meters.angle()
print(angle)  # Output: 53.13010235415599 degrees
```