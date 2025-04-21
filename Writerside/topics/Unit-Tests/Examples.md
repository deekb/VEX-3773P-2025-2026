# Unit Test Examples

## Example: Generic Odometry Unit Test

Below is the full code for the `TestGenericOdometry` unit test, which tests the `GenericOdometry` class. The test ensures that the odometry calculations are accurate under various scenarios, including edge cases and extreme movements.

```python
# ...existing code from the example in the original file...
```

### Explanation of the Code:

1. **Imports**: The test imports necessary modules, including `unittest`, `math`, and mock utilities.
2. **Setup**: The `setUpClass` and `setUp` methods initialize the mock sensor and odometry object.
3. **Helper Methods**: `assertPoseAlmostEqual` and `_update_and_assert_pose` simplify repetitive assertions.
4. **Test Cases**: Each `test_` method validates specific functionality, such as pose updates, rotations, and edge cases.
5. **Execution**: The `unittest.main()` call allows the test to be run directly.
