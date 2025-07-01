# Rotation2d Class

Represents a 2D rotation.

## Features

- **Create** a `Rotation2d` object from radians, degrees, or revolutions using the `from_<unit>` class methods. This is the most explicit and least error-prone way to use the class.
- **Add** or **subtract** two `Rotation2d` objects.
- **Multiply** or **divide** a `Rotation2d` object by a scalar.
- **Check equality** between two `Rotation2d` objects.
- **Convert** the angle to radians, degrees, or revolutions.
- **Calculate the sine, cosine, tangent, and their hyperbolic counterparts** of the angle.
- **Calculate the inverse** of a `Rotation2d` object.
- **Normalize** the rotation angle to the range -π to π radians.
- **Interpolate** between two `Rotation2d` objects.
### Imports

```python
from VEXLib.Geometry.Rotation2d import Rotation2d
```

### Usage Examples

#### Create a Rotation2d object from different units

```python
rotation_radians = Rotation2d.from_radians(1.57)
print(rotation_radians)  # Output: 1.57 radians

rotation_degrees = Rotation2d.from_degrees(90)
print(rotation_degrees)  # Output: 1.5707963267948966 radians

rotation_revolutions = Rotation2d.from_revolutions(0.25)
print(rotation_revolutions)  # Output: 1.5707963267948966 radians
```

#### Add two Rotation2d objects

```python
sum_rotation = rotation_radians + rotation_degrees
print(sum_rotation)  # Output: 3.1407963267948966 radians
```

#### Subtract two Rotation2d objects

```python
difference_rotation = rotation_radians - rotation_degrees
print(difference_rotation)  # Output: 0.0 radians
```

#### Multiply a Rotation2d object by a scalar

```python
scaled_rotation = rotation_radians * 2
print(scaled_rotation)  # Output: 3.14 radians
```

#### Divide a Rotation2d object by a scalar

```python
divided_rotation = rotation_radians / 2
print(divided_rotation)  # Output: 0.785 radians
```

#### Check equality between two Rotation2d objects

```python
are_equal = rotation_radians == rotation_degrees
print(are_equal)  # Output: True
```

#### Convert the angle to different units

```python
print(rotation_radians.to_degrees())     # Output: 90.0
print(rotation_radians.to_revolutions()) # Output: 0.25
```

#### Calculate the sine, cosine, and tangent of the angle

```python
print(rotation_radians.sin())  # Output: 1.0
print(rotation_radians.cos())  # Output: 0.0
print(rotation_radians.tan())  # Output: 16331239353195370.0
```

#### Calculate the inverse of a Rotation2d object

```python
inverse_rotation = rotation_radians.inverse()
print(inverse_rotation)  # Output: -1.57 radians
```

#### Normalize the rotation angle

```python
normalized_rotation = rotation_radians.normalize()
print(normalized_rotation)  # Output: 1.57 radians
```

#### Interpolate between two Rotation2d objects

```python
interpolated_rotation = rotation_radians.interpolate(rotation_degrees, 0.5)
print(interpolated_rotation)  # Output: 1.57 radians
```

## Explanation of Normalization

The normalization process for a `Rotation2d` object involves adjusting the rotation angle to ensure it falls within the range of -π to π radians. This is useful for maintaining consistency and avoiding issues with angles that exceed a full circle 2π radians).`Rotation2d` object will have an angle that is easy to work with and avoids complications from angles that are too large or too small.