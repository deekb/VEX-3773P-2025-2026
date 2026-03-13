# python
import math
from VEXLib.Math.Matrix import Matrix, Shape

class PoseEKF:
    """
    EKF for 2D pose with velocity and yaw-rate.
    State: [x, y, theta, v, omega] (column Matrix Shape(1,5))
    Measurements: [x, y, theta] (direct)
    Uses only `math` and `VEXLib.Math.Matrix`.
    """

    def __init__(self, Q=None, R=None, P=None, x0=None):
        self.n = 5
        self.m = 3
        # state column (1 column, n rows)
        if x0 is None:
            x0 = [0.0] * self.n
        self.x = self._ensure_col(x0, expected_rows=self.n)

        # default covariances
        self.Q = Q if Q is not None else Matrix(Shape(self.n, self.n),
                                               data=[[1e-3 if i == j else 0.0 for i in range(self.n)] for j in range(self.n)])
        self.R = R if R is not None else Matrix(Shape(self.m, self.m),
                                               data=[[1e-2 if i == j else 0.0 for i in range(self.m)] for j in range(self.m)])
        self.P = P if P is not None else Matrix.identity(self.n)

        # measurement matrix H (m rows, n cols) => Shape(n_cols, m_rows) == Shape(self.n, self.m)
        H_data = [
            [1.0, 0.0, 0.0, 0.0, 0.0],  # x
            [0.0, 1.0, 0.0, 0.0, 0.0],  # y
            [0.0, 0.0, 1.0, 0.0, 0.0],  # theta
        ]
        self.H = Matrix(Shape(self.n, self.m), H_data)

    # --------------------
    # Public API
    # --------------------
    def predict(self, dt):
        """
        Nonlinear predict step with constant-velocity + yaw-rate model:
          x' = x + v * cos(theta) * dt
          y' = y + v * sin(theta) * dt
          theta' = theta + omega * dt
          v' = v
          omega' = omega
        """
        # extract current values
        x = float(self.x.data[0][0])
        y = float(self.x.data[1][0])
        th = float(self.x.data[2][0])
        v = float(self.x.data[3][0])
        w = float(self.x.data[4][0])

        # predict state
        nx = x + v * math.cos(th) * dt
        ny = y + v * math.sin(th) * dt
        nth = th + w * dt
        nv = v
        nw = w
        self.x = self._ensure_col([nx, ny, nth, nv, nw], expected_rows=self.n)
        self.x.data[2][0] = self._wrap_angle(self.x.data[2][0])

        # Jacobian F (5x5)
        F = [[0.0]*self.n for _ in range(self.n)]
        # fill identity-ish
        for i in range(self.n):
            F[i][i] = 1.0
        # partials
        F[0][2] = -v * math.sin(th) * dt  # dx/dtheta
        F[0][3] = math.cos(th) * dt       # dx/dv
        F[1][2] = v * math.cos(th) * dt   # dy/dtheta
        F[1][3] = math.sin(th) * dt       # dy/dv
        F[2][4] = dt                      # dtheta/domega

        Fmat = Matrix(Shape(self.n, self.n), F)

        # P = F P F^T + Q
        Ft = self._transpose(Fmat)
        self.P = (Fmat * self.P * Ft) + self.Q

    def update(self, z):
        """
        Measurement z = [x_meas, y_meas, theta_meas]
        """
        z_col = self._ensure_col(z, expected_rows=self.m)
        # predicted measurement
        z_pred = self.H * self.x  # column (m x 1)

        # innovation y = z - z_pred (wrap theta residual)
        y = z_col - z_pred
        # wrap angle residual (third row)
        y.data[2][0] = self._wrap_angle(y.data[2][0])

        # S = H P H^T + R
        S = (self.H * self.P * self._transpose(self.H)) + self.R
        S_inv = S.inverse()

        # K = P H^T S^{-1}
        K = self.P * self._transpose(self.H) * S_inv

        # x = x + K y
        self.x = self.x + (K * y)
        # wrap theta
        self.x.data[2][0] = self._wrap_angle(self.x.data[2][0])

        # P = (I - K H) P
        I = Matrix.identity(self.n)
        self.P = (I - (K * self.H)) * self.P

    def state(self):
        """Return [x,y,theta,v,omega] as list"""
        return [self.x.data[i][0] for i in range(self.n)]

    # --------------------
    # Helpers
    # --------------------
    def _ensure_col(self, v, expected_rows=None):
        if isinstance(v, Matrix):
            if expected_rows is not None and v.shape.y_size != expected_rows:
                raise ValueError("Matrix rows mismatch")
            return v
        if not isinstance(v, (list, tuple)):
            raise TypeError("Vector must be list/tuple or Matrix")
        if expected_rows is not None and len(v) != expected_rows:
            raise ValueError("Vector length mismatch")
        data = [[float(val)] for val in v]
        return Matrix(Shape(1, len(v)), data)

    def _transpose(self, mat):
        rows = mat.shape.y_size
        cols = mat.shape.x_size
        transposed = [[mat.data[r][c] for r in range(rows)] for c in range(cols)]
        return Matrix(Shape(rows, cols), transposed)

    def _wrap_angle(self, a):
        # normalize to [-pi, pi)
        a = (a + math.pi) % (2.0 * math.pi) - math.pi
        return a
