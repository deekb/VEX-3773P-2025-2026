# python
import math
from VEXLib.Math.Matrix import Matrix, Shape

class KalmanFilter:
    """
    Discrete linear Kalman filter using only math and `VEXLib/Math/Matrix.py`.

    State vector is represented as a column Matrix of shape (1, n) (1 column, n rows).
    Matrices follow the same Shape(x_size=columns, y_size=rows) convention from Matrix.py.

    Basic equations used:
      x = F x + B u
      P = F P F^T + Q
      y = z - H x
      S = H P H^T + R
      K = P H^T S^{-1}
      x = x + K y
      P = (I - K H) P
    """

    def __init__(self, n, m=None, F=None, H=None, Q=None, R=None, P=None, B=None, x0=None):
        """
        Args:
          n (int): state dimension
          m (int|None): measurement dimension; defaults to n if None
          F, H, Q, R, P, B (Matrix|None): optional initial matrices (must match shapes)
          x0 (list|Matrix|None): initial state (list length n or column Matrix)
        """
        self.n = int(n)
        self.m = int(m if m is not None else n)

        # Default matrices
        self.F = F if F is not None else Matrix.identity(self.n)
        if H is None:
            if self.m != self.n:
                raise ValueError("Measurement matrix H must be provided when m != n")
            self.H = Matrix.identity(self.n)
        else:
            self.H = H

        self.Q = Q if Q is not None else Matrix(Shape(self.n, self.n), data=[[0.0]*self.n for _ in range(self.n)])
        self.R = R if R is not None else Matrix(Shape(self.m, self.m), data=[[0.0]*self.m for _ in range(self.m)])
        self.P = P if P is not None else Matrix.identity(self.n)
        self.B = B  # optional control matrix mapping control (l) -> state
        self.x = self._ensure_col(x0 if x0 is not None else [0.0]*self.n)

    # --------------------
    # Public API
    # --------------------
    def predict(self, u=None):
        """
        Predict step. Optional control vector u (list or column Matrix).
        """
        if u is not None and self.B is None:
            raise ValueError("Control provided but B matrix is not set")
        # x = F * x + B * u
        self.x = self.F * self.x
        if u is not None:
            u_col = self._ensure_col(u)
            self.x = self.x + (self.B * u_col)
        # P = F * P * F^T + Q
        self.P = (self.F * self.P * self._transpose(self.F)) + self.Q

    def update(self, z):
        """
        Update step with measurement z (list length m or column Matrix).
        """
        z_col = self._ensure_col(z, expected_rows=self.m)
        # y = z - H * x
        y = z_col - (self.H * self.x)
        # S = H P H^T + R
        S = (self.H * self.P * self._transpose(self.H)) + self.R
        # K = P H^T S^{-1}
        S_inv = S.inverse()
        K = self.P * self._transpose(self.H) * S_inv
        # x = x + K y
        self.x = self.x + (K * y)
        # P = (I - K H) P
        I = Matrix.identity(self.n)
        self.P = (I - (K * self.H)) * self.P

    def set_matrices(self, **kwargs):
        """Set any of F, H, Q, R, P, B, x (pass Matrix or lists)."""
        for k, v in kwargs.items():
            if k == "x":
                self.x = self._ensure_col(v)
            elif v is not None:
                setattr(self, k, v)

    def state(self):
        """Return current state as list of length n."""
        return self._col_to_list(self.x)

    # --------------------
    # Helpers
    # --------------------
    def _ensure_col(self, v, expected_rows=None):
        """
        Convert list or Matrix to column Matrix shape (1, n).
        If v is already a Matrix, validates shape.
        """
        if isinstance(v, Matrix):
            if expected_rows is not None and v.shape.y_size != expected_rows:
                raise ValueError("Matrix rows mismatch")
            return v
        if not isinstance(v, (list, tuple)):
            raise TypeError("Vector must be list/tuple or Matrix")
        if expected_rows is not None and len(v) != expected_rows:
            raise ValueError("Vector length mismatch")
        # build column matrix (one element per row)
        data = [[float(val)] for val in v]
        return Matrix(Shape(1, len(v)), data)

    def _col_to_list(self, mat):
        """Convert a column Matrix (1, n) to list length n."""
        return [row[0] for row in mat.data]

    def _transpose(self, mat):
        """Return transpose of a Matrix."""
        rows = mat.shape.y_size
        cols = mat.shape.x_size
        transposed = [[mat.data[r][c] for r in range(rows)] for c in range(cols)]
        return Matrix(Shape(rows, cols), transposed)
