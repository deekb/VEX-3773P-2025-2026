# Unit Test Structure

## Test Structure:

- Each test file contains one or more test classes that inherit from `unittest.TestCase`.
- Test methods within these classes are prefixed with `test_` to be automatically discovered by the test runner.

## Test Coverage:

The tests cover a wide range of functionality, including:

- **Mathematical Utilities**: Functions like clamping, interpolation, and angle normalization.
- **Geometry**: Classes like `Pose2d`, `Translation2d`, and `Rotation2d` are tested for operations like addition, subtraction, and transformations.
- **Algorithms**: Components like `SlewRateLimiter` and `GenericOdometry` are tested for correctness under various scenarios.
- **Serial Communication**: The `SerialFrame` class is tested for encoding, decoding, and error handling.
- **Robot Logic**: The `TickBasedRobot` class is tested for state transitions and callback execution.
