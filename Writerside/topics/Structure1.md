# Unit Test Structure

## Test Structure:

- Each test file contains one or more test classes that inherit from `unittest.TestCase`.
- Test methods within these classes are prefixed with `test_` to be automatically discovered by the test runner.

```python
import unittest
# import the modules you will be testing


class TestComponent(unittest.TestCase):
    def test_functionality(self):
        # Check whether two objects are equal
        self.assertEqual(2, 2)
        # Check whether two objects are almost equal
        self.assertAlmostEqual(3.0000008, 3, places=6)
    
if __name__ == '__main__':
    unittest.main()
```