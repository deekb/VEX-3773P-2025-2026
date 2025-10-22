import math
import random

class Shape:
    """
    Represents a 2D shape or matrix dimensions.

    Attributes:
        x_size (int): Number of columns (width). Must be positive.
        y_size (int): Number of rows (height). Must be positive.
    """

    def __init__(self, x_size, y_size):
        """
        Initialize a Shape with width and height.

        Args:
            x_size (int): Number of columns. Must be positive.
            y_size (int): Number of rows. Must be positive.

        Raises:
            ValueError: If x_size or y_size is not a positive integer.
        """
        if not isinstance(x_size, int) or not isinstance(y_size, int) or x_size <= 0 or y_size <= 0:
            raise ValueError("x_size and y_size must both be positive integers")
        self._x_size = x_size
        self._y_size = y_size

    @property
    def x_size(self):
        """int: Get or set the number of columns."""
        return self._x_size

    @x_size.setter
    def x_size(self, x_size):
        if not isinstance(x_size, int) or x_size <= 0:
            raise ValueError("x_size must be a positive integer")
        self._x_size = x_size

    @property
    def y_size(self):
        """int: Get or set the number of rows."""
        return self._y_size

    @y_size.setter
    def y_size(self, y_size):
        if not isinstance(y_size, int) or y_size <= 0:
            raise ValueError("y_size must be a positive integer")
        self._y_size = y_size

    def __repr__(self):
        return f"<Shape x_size={self._x_size}, y_size={self._y_size}>"

    def __copy__(self):
        return Shape(self.x_size, self.y_size)


class Matrix:
    """
    Represents a 2D matrix and supports common linear algebra operations.

    Attributes:
        shape (Shape): Shape of the matrix.
        data (list[list[float]]): 2D list storing matrix elements.
    """

    def __init__(self, shape, data=None):
        """
        Initialize a Matrix with given shape and optional data.

        Args:
            shape (Shape): Shape of the matrix.
            data (list[list[float]], optional): Matrix values. If None, initializes to zeros.

        Raises:
            ValueError: If shape has non-positive dimensions.
        """
        if shape.x_size <= 0 or shape.y_size <= 0:
            raise ValueError("Minimum matrix size is 1x1")
        self.shape = shape
        if data is None:
            self.data = []
            self.clear()
        else:
            self.data = data

    # -------------------------------
    # Printing and Formatting
    # -------------------------------

    def pretty(self, precision=4):
        """
        Return a formatted string representation of the matrix.

        Args:
            precision (int): Number of decimal places to display.

        Returns:
            str: Formatted string of the matrix with aligned columns.
        """
        str_rows = [
            [f"{val:.{precision}f}" for val in row] for row in self.data
        ]
        col_widths = [
            max(len(str_rows[r][c]) for r in range(len(str_rows)))
            for c in range(len(str_rows[0]))
        ]
        lines = []
        for row in str_rows:
            line = (
                "[ "
                + "  ".join(f"{val:>{col_widths[i]}}" for i, val in enumerate(row))
                + " ]"
            )
            lines.append(line)
        return "\n".join(lines)

    def __repr__(self):
        return self.pretty()

    def __str__(self):
        return self.pretty()

    # -------------------------------
    # Class Methods
    # -------------------------------

    @classmethod
    def identity(cls, size):
        """
        Create an identity matrix of given size.

        Args:
            size (int): Number of rows and columns. Must be >= 1.

        Returns:
            Matrix: Identity matrix of shape size x size.

        Raises:
            ValueError: If size < 1.
        """
        if size < 1:
            raise ValueError("Size must be at least 1")
        data = [[1 if i == j else 0 for i in range(size)] for j in range(size)]
        return cls(shape=Shape(size, size), data=data)

    # -------------------------------
    # Data Manipulation
    # -------------------------------

    def clear(self):
        """Set all elements of the matrix to zero."""
        self.fill_with(0)

    def transpose(self):
        """
        Return the transposed matrix (rows and columns swapped).
        """
        y = self.shape.y_size  # original number of rows
        x = self.shape.x_size  # original number of columns
        transposed_data = [[self.data[r][c] for r in range(y)] for c in range(x)]
        return Matrix(Shape(y, x), transposed_data)

    def fill_with_random(self):
        """Fill the matrix with random values in the range [-1, 1]."""
        self.data = [
            [(random.random() * 2) - 1 for _ in range(self.shape.x_size)]
            for _ in range(self.shape.y_size)
        ]

    def fill_with(self, value):
        """
        Fill the matrix with a specific value.

        Args:
            value (float): Value to fill the matrix with.
        """
        self.data = [[value] * self.shape.x_size for _ in range(self.shape.y_size)]

    def is_square(self):
        """
        Check if the matrix is square.

        Returns:
            bool: True if square, False otherwise.
        """
        return self.shape.x_size == self.shape.y_size

    def is_same_shape_as(self, other):
        """
        Check if another matrix has the same shape.

        Args:
            other (Matrix): Matrix to compare with.

        Returns:
            bool: True if same shape, False otherwise.
        """
        return self.shape.x_size == other.shape.x_size and self.shape.y_size == other.shape.y_size

    # -------------------------------
    # Element Access
    # -------------------------------

    def set_at(self, position, value):
        """
        Set a value at a specific row and column.

        Args:
            position (tuple[int, int]): (row, column) index.
            value (float): Value to set.
        """
        row_number, column_number = position
        self.data[row_number][column_number] = value

    def get_at(self, position):
        """
        Get a value at a specific row and column.

        Args:
            position (tuple[int, int]): (row, column) index.

        Returns:
            float: Value at the specified position.
        """
        row_number, column_number = position
        return self.data[row_number][column_number]

    # -------------------------------
    # Arithmetic Operators
    # -------------------------------

    def __add__(self, other):
        if not self.is_same_shape_as(other):
            raise ValueError("Shape mismatch")
        added_matrix_data = [
            [x1 + x2 for x1, x2 in zip(r1, r2)]
            for r1, r2 in zip(self.data, other.data)
        ]
        return Matrix(self.shape, added_matrix_data)

    def __sub__(self, other):
        if not self.is_same_shape_as(other):
            raise ValueError("Shape mismatch")
        sub_data = [
            [x1 - x2 for x1, x2 in zip(r1, r2)]
            for r1, r2 in zip(self.data, other.data)
        ]
        return Matrix(self.shape, sub_data)

    def __mul__(self, other):
        if isinstance(other, (list, tuple)):
            if len(other) != self.shape.x_size:
                raise ValueError("Vector length mismatch")
            return [sum(a * b for a, b in zip(row, other)) for row in self.data]
        if isinstance(other, Matrix):
            if self.shape.x_size != other.shape.y_size:
                raise ValueError("Matrix size mismatch for multiplication")

            result = [
                [sum(self.data[i][k] * other.data[k][j] for k in range(self.shape.x_size))
                 for j in range(other.shape.x_size)]
                for i in range(self.shape.y_size)
            ]
            return Matrix(Shape(other.shape.x_size, self.shape.y_size), result)
        elif isinstance(other, (int, float)):
            return Matrix(self.shape, [[x * other for x in row] for row in self.data])
        else:
            raise TypeError("Unsupported operand for multiplication")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Matrix(self.shape, [[x / other for x in row] for row in self.data])
        else:
            raise TypeError("Matrix division only supports scalars")

    # -------------------------------
    # 3D Rotations
    # -------------------------------

    @staticmethod
    def rotation_x(theta):
        """
        Create a 3x3 rotation matrix around the X-axis.

        Args:
            theta (float): Angle in radians.

        Returns:
            Matrix: 3x3 rotation matrix.
        """
        c, s = math.cos(theta), math.sin(theta)
        return Matrix(Shape(3, 3), [[1, 0, 0], [0, c, -s], [0, s, c]])

    @staticmethod
    def rotation_y(theta):
        """
        Create a 3x3 rotation matrix around the Y-axis.

        Args:
            theta (float): Angle in radians.

        Returns:
            Matrix: 3x3 rotation matrix.
        """
        c, s = math.cos(theta), math.sin(theta)
        return Matrix(Shape(3, 3), [[c, 0, s], [0, 1, 0], [-s, 0, c]])

    @staticmethod
    def rotation_z(theta):
        """
        Create a 3x3 rotation matrix around the Z-axis.

        Args:
            theta (float): Angle in radians.

        Returns:
            Matrix: 3x3 rotation matrix.
        """
        c, s = math.cos(theta), math.sin(theta)
        return Matrix(Shape(3, 3), [[c, -s, 0], [s, c, 0], [0, 0, 1]])

    # -------------------------------
    # Copying
    # -------------------------------

    def copy(self):
        """Return a deep copy of the matrix."""
        return Matrix(self.shape, [row[:] for row in self.data])

    # -------------------------------
    # Linear Algebra
    # -------------------------------

    def determinant(self):
        """
        Compute the determinant of a square matrix using Gaussian elimination.

        Returns:
            float: Determinant value.

        Raises:
            ValueError: If matrix is not square.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square")

        m = [row[:] for row in self.data]
        n = self.shape.x_size
        det = 1
        swaps = 0

        for i in range(n):
            pivot = i
            for j in range(i + 1, n):
                if abs(m[j][i]) > abs(m[pivot][i]):
                    pivot = j
            if pivot != i:
                m[i], m[pivot] = m[pivot], m[i]
                swaps += 1
            if m[i][i] == 0:
                return 0
            det *= m[i][i]
            for j in range(i + 1, n):
                ratio = m[j][i] / m[i][i]
                for k in range(i, n):
                    m[j][k] -= ratio * m[i][k]

        if swaps % 2:
            det = -det
        return det

    def inverse(self):
        """
        Compute the inverse of a square matrix using Gauss-Jordan elimination.

        Returns:
            Matrix: Inverse matrix.

        Raises:
            ValueError: If matrix is not square or singular.
        """
        if not self.is_square():
            raise ValueError("Matrix must be square to invert")

        n = self.shape.x_size
        A = [row[:] for row in self.data]
        I = Matrix.identity(n).data

        # Forward elimination
        for i in range(n):
            pivot = A[i][i]
            if pivot == 0:
                # Find nonzero pivot below
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        I[i], I[j] = I[j], I[i]
                        break
                else:
                    raise ValueError("Matrix is singular and cannot be inverted")

            # Normalize pivot row
            factor = A[i][i]
            A[i] = [x / factor for x in A[i]]
            I[i] = [x / factor for x in I[i]]

            # Eliminate other rows
            for j in range(n):
                if j != i:
                    ratio = A[j][i]
                    A[j] = [a - ratio * b for a, b in zip(A[j], A[i])]
                    I[j] = [a - ratio * b for a, b in zip(I[j], I[i])]

        return Matrix(Shape(n, n), I)

    def jacobian(self, func, epsilon=1e-6):
        """
        Compute the Jacobian matrix of a vector-valued function at the current matrix treated as a vector.

        Args:
            func (callable): A function that takes a 1D list of length n (flattened matrix) and returns a list of length m.
            epsilon (float): Small step size for numerical derivative approximation.

        Returns:
            Matrix: m x n Jacobian matrix.

        Example:
            # f: R^2 -> R^2
            def f(x):
                return [x[0]**2 + x[1], x[0] - x[1]**2]

            mat = Matrix(Shape(2, 1), data=[[1], [2]])  # Column vector
            J = mat.jacobian(f)
        """
        # Flatten the matrix as a 1D vector
        x_flat = [self.data[r][c] for r in range(self.shape.y_size) for c in range(self.shape.x_size)]
        n = len(x_flat)
        f0 = func(x_flat)
        m = len(f0)
        J_data = [[0.0 for _ in range(n)] for _ in range(m)]

        for j in range(n):
            x_eps = x_flat[:]
            x_eps[j] += epsilon
            f_eps = func(x_eps)
            for i in range(m):
                J_data[i][j] = (f_eps[i] - f0[i]) / epsilon

        return Matrix(Shape(n, m).copy(), [list(row) for row in J_data])


# -------------------------------
# TEST: Inverse correctness
# -------------------------------
if __name__ == "__main__":
    print("Testing matrix inverse...\n")

    A = Matrix(Shape(3, 3), data=[
        [40, 7, 2],
        [3, 6, 1],
        [2, 5, 3]
    ])
    A_inv = A.inverse()
    result = A * A_inv

    print("A:")
    print(A)
    print("\nA⁻¹:")
    print(A_inv)
    print("\nA * A⁻¹ (should be identity):")
    print(result.pretty(4))

    # Numerical check
    identity = Matrix.identity(4)
    close_enough = all(abs(result.data[i][j] - identity.data[i][j]) < 1e-6 for i in range(3) for j in range(3))
    print("\nInverse test passed:", close_enough)
