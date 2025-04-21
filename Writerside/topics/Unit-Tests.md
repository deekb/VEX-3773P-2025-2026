# Unit Tests

![Unit Tests](software_tests.png)

Unit testing is a software development practice where individual components or functions of a program are tested in isolation to ensure they work as expected. These tests are typically automated and focus on verifying the correctness of small, self-contained units of code.

## Test Framework:

The repository uses Python's built-in [`unittest`](https://docs.python.org/3/library/unittest.html) framework for writing and running tests.

## Test Organization:

- Tests are organized into separate files under the [`tests`](https://github.com/deekb/VEXlib/tree/master/tests) directory.
- Each file typically corresponds to a specific module or functionality (e.g., `TestMathUtil.py` for math utilities, `TestPose2d.py` for 2D pose operations).

## Running Tests:

### In PyCharm:

1. Open the project in PyCharm.
2. Navigate to the `tests` directory in the Project Explorer.
3. Right-click on a test file or the `tests` directory and select **Run 'Unittests in...'**.
4. View the test results in the Run or Test Runner tab.

### On Windows/Linux/Mac Without an IDE:

1. Open a terminal or command prompt.
2. Navigate to the root directory of the project (e.g., `/home/derek/PycharmProjects/VEXlib`).
3. Run the following command to execute all tests:
   ```bash
   python -m unittest discover -s tests
   ```
4. To run a specific test file, use:
   ```bash
   python -m unittest tests.<test_file_name>
   ```
   Replace `<test_file_name>` with the name of the test file (e.g., `TestKinematicsUtil`).

5. For more detailed output, add the `-v` flag:
   ```bash
   python -m unittest discover -s tests -v
   ```

Unit testing is a cornerstone of robust software development, ensuring that individual components function correctly and enabling developers to build reliable and maintainable systems.
