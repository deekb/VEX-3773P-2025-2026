# Translation1d Class

Represents a 1D translation.

## Features

- **Create** a `Translation1d` object from meters, centimeters, inches, or feet using the `from_<unit>` class methods. This is the most explicit and least error-prone way to use the class.
- **Add** or **subtract** two `Translation1d` objects.
- **Multiply** or **divide** a `Translation1d` object by a scalar.
- **Check equality** between two `Translation1d` objects.
- **Convert** the magnitude to meters, centimeters, inches, or feet.
- **Calculate the inverse** of a `Translation1d` object.

## Examples

### Create a Translation1d object from different units

```python
from VEXLib.Geometry.Translation1d import Translation1d

translation_meters = Translation1d.from_meters(5)
print(translation_meters)  # Output: 5m

translation_centimeters = Translation1d.from_centimeters(500)
print(translation_centimeters)  # Output: 5m

translation_inches = Translation1d.from_inches(196.85)
print(translation_inches)  # Output: 5m

translation_feet = Translation1d.from_feet(16.4042)
print(translation_feet)  # Output: 5m
```

### Add two Translation1d objects

```python
sum_translation = translation_meters + translation_centimeters
print(sum_translation)  # Output: 10m
```

### Subtract two Translation1d objects

```python
difference_translation = translation_meters - translation_centimeters
print(difference_translation)  # Output: 0m
```

### Multiply a Translation1d object by a scalar

```python
scaled_translation = translation_meters * 2
print(scaled_translation)  # Output: 10m
```

### Divide a Translation1d object by a scalar

```python
divided_translation = translation_meters / 2
print(divided_translation)  # Output: 2.5m
```

### Check equality between two Translation1d objects

```python
are_equal = translation_meters == translation_centimeters
print(are_equal)  # Output: True
```

### Convert the magnitude to different units

```python
print(translation_meters.to_centimeters())  # Output: 500.0
print(translation_meters.to_inches())       # Output: 196.8503937007874
print(translation_meters.to_feet())         # Output: 16.404199475065616
```

### Calculate the inverse of a Translation1d object

```python
inverse_translation = translation_meters.inverse()
print(inverse_translation)  # Output: -5m