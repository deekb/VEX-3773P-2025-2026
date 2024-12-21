# Pose2d Class

Represents a 2D pose composed of a `Translation2d` and a `Rotation2d`.

## Features

- **Create** a `Pose2d` object with translation and rotation.
- **Add** or **subtract** two `Pose2d` objects.
- **Multiply** a `Pose2d` object by a scalar.
- **Check equality** between two `Pose2d` objects.
- **String representation** of a `Pose2d` object.
- **Create** a `Pose2d` object from given `Translation2d` and `Rotation2d` objects.
- **Create** a `Pose2d` object with zero translation and rotation.
- **Create** a `Pose2d` object from a `Translation2d` object assuming the rotation is zero radians by default.
- **Create** a `Pose2d` object from a `Rotation2d` object assuming the translation is (0, 0) meters by default.



### Imports

```python
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Pose2d import Pose2d
```

### Usage Examples

#### Create a Pose2d object

```python
translation = Translation2d.from_meters(3, 4)
rotation = Rotation2d.from_degrees(90)
pose = Pose2d(translation, rotation)
print(pose)  # Output: Translation: (3m, 4m), Rotation: 1.5707963267948966 radians
```

#### Add two Pose2d objects

```python
pose1 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d.from_degrees(90))
pose2 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d.from_degrees(45))
sum_pose = pose1 + pose2
print(sum_pose)  # Output: Translation: (4m, 6m), Rotation: 2.356194490192345 radians
```

#### Subtract two Pose2d objects

```python
pose1 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d.from_degrees(90))
pose2 = Pose2d(Translation2d.from_meters(1, 2), Rotation2d.from_degrees(45))
difference_pose = pose1 - pose2
print(difference_pose)  # Output: Translation: (2m, 2m), Rotation: 0.7853981633974483 radians
```

#### Multiply a Pose2d object by a scalar

```python
pose = Pose2d(Translation2d.from_meters(3, 4), Rotation2d.from_degrees(90))
scaled_pose = pose * 2
print(scaled_pose)  # Output: Translation: (6m, 8m), Rotation: 3.141592653589793 radians
```

#### Check equality between two Pose2d objects

```python
pose1 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d.from_degrees(90))
pose2 = Pose2d(Translation2d.from_meters(3, 4), Rotation2d.from_degrees(90))
are_equal = pose1 == pose2
print(are_equal)  # Output: True
```

#### Create a Pose2d object with zero translation and rotation

```python
zero_pose = Pose2d.from_zero()
print(zero_pose)  # Output: Translation: (0m, 0m), Rotation: 0.0 radians
```

#### Create a Pose2d object from a Translation2d object

```python
translation = Translation2d.from_meters(3, 4)
pose = Pose2d.from_translation2d(translation)
print(pose)  # Output: Translation: (3m, 4m), Rotation: 0.0 radians
```

#### Create a Pose2d object from a Rotation2d object

```python
rotation = Rotation2d.from_degrees(90)
pose = Pose2d.from_rotation2d(rotation)
print(pose)  # Output: Translation: (0m, 0m), Rotation: 1.5707963267948966 radians
```