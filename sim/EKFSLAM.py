# python
# File: sim/EKFSLAMSimulation.py
import math
import random
import pygame
from VEXLib.Math.Matrix import Matrix, Shape

# -----------------------
# Helpers
# -----------------------
def diag_matrix(size, var):
    return Matrix(Shape(size, size),
                  data=[[var if i == j else 0.0 for j in range(size)] for i in range(size)])

# python
def transpose(mat):
    # prefer native transpose if provided by the Matrix class
    if hasattr(mat, "_transpose"):
        try:
            return mat._transpose()
        except Exception:
            pass

    # try to infer dimensions from shape, fallback to data lengths
    try:
        rows = int(mat.shape.y_size)
        cols = int(mat.shape.x_size)
    except Exception:
        rows = len(mat.data) if getattr(mat, "data", None) else 0
        cols = len(mat.data[0]) if rows > 0 else 0

    # build transposed with safe indexing
    transposed = []
    for c in range(cols):
        row = []
        for r in range(rows):
            try:
                row.append(mat.data[r][c])
            except Exception:
                # fallback: try column-major storage
                try:
                    row.append(mat.data[c][r])
                except Exception:
                    row.append(0.0)
        transposed.append(row)

    return Matrix(Shape(cols, rows), transposed)


def eig2(a, b, c, d):
    tr = a + d
    det = a * d - b * c
    mid = tr * 0.5
    disc = max(0.0, mid * mid - det)
    s = math.sqrt(disc)
    l1 = mid + s
    l2 = mid - s
    if abs(b) > 1e-12 or abs(a - l1) > 1e-12:
        v1 = (b, l1 - a)
    else:
        v1 = (l1 - d, c)
    mag = math.hypot(v1[0], v1[1]) or 1.0
    v1 = (v1[0] / mag, v1[1] / mag)
    return l1, l2, v1

def draw_cov_ellipse(surface, center_px, cov_2x2, scale, color=(80,140,255,60)):
    a = cov_2x2[0][0]; b = cov_2x2[0][1]; c = cov_2x2[1][0]; d = cov_2x2[1][1]
    l1, l2, v1 = eig2(a, b, c, d)
    chi2_95 = 5.991
    r1 = math.sqrt(max(0.0, l1 * chi2_95)) * scale
    r2 = math.sqrt(max(0.0, l2 * chi2_95)) * scale
    w = max(2, int(2 * r1)); h = max(2, int(2 * r2))
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, color, (0, 0, w - 1, h - 1))
    angle = math.degrees(math.atan2(v1[1], v1[0]))
    rot = pygame.transform.rotate(surf, -angle)
    rect = rot.get_rect(center=center_px)
    surface.blit(rot, rect)

def wrap_angle(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi

# -----------------------
# EKF-SLAM class
# -----------------------
class EKFSLAM:
    """
    Range-only EKF-SLAM (2D) - optimized for runtime:
      * caps number of landmarks with `max_landmarks`
      * ignores very short/invalid ranges (`min_init_range`)
      * uses a tighter default gating (1-DOF 95% = 3.84)
      * simple oldest-landmark pruning when cap exceeded
      * local-variable micro-optimizations in heavy loops
    State layout same as before:
      x = [xr, yr, theta, l1x, l1y, l2x, l2y, ...]^T
    """
    def __init__(self, Q=None, P0=None, max_landmarks=60, min_init_range=0.1):
        self.n_robot = 3
        self.x = Matrix(Shape(1, self.n_robot), data=[[0.0], [0.0], [0.0]])
        if P0 is None:
            self.P = Matrix.identity(self.n_robot)
        else:
            self.P = P0
        if Q is None:
            self.Q = diag_matrix(self.n_robot, 1e-3)
        else:
            self.Q = Q
        self.num_landmarks = 0
        self.max_landmarks = int(max_landmarks)
        self.min_init_range = float(min_init_range)

    @property
    def dim(self):
        return self.x.shape.y_size

    def predict(self, v, w, dt):
        xr = float(self.x.data[0][0]); yr = float(self.x.data[1][0]); th = float(self.x.data[2][0])
        nxr = xr + v * math.cos(th) * dt
        nyr = yr + v * math.sin(th) * dt
        nth = wrap_angle(th + w * dt)

        landmark_part = []
        for i in range(self.num_landmarks * 2):
            landmark_part.append(self.x.data[3 + i][0])
        self.x = self._ensure_col([nxr, nyr, nth] + landmark_part)

        F = [[0.0]*self.dim for _ in range(self.dim)]
        for i in range(self.dim):
            F[i][i] = 1.0
        F[0][2] = -v * math.sin(th) * dt
        F[1][2] = v * math.cos(th) * dt

        Fmat = Matrix(Shape(self.dim, self.dim), F)
        Ft = self._transpose(Fmat)

        Qbig = Matrix(Shape(self.dim, self.dim), data=[[0.0]*self.dim for _ in range(self.dim)])
        for i in range(self.n_robot):
            for j in range(self.n_robot):
                Qbig.data[i][j] = self.Q.data[i][j]

        self.P = (Fmat * self.P * Ft) + Qbig

    def update_ranges(self, ranges, bearings, R_range, gating_thresh=3.84):
        """
        Sequentially process range beams. Default gating is 3.84 (1-DOF ~95%).
        Avoids initializing landmarks when range < min_init_range or when cap reached.
        """
        for r_meas, b in zip(ranges, bearings):
            # skip very small/noisy readings
            if r_meas <= 0.0 or r_meas < self.min_init_range:
                continue

            best_idx = None
            best_mahal = float('inf')
            best_H = None
            best_Sval = None
            best_dist = None

            # local references for speed
            P_data = self.P.data
            dim = self.dim
            num_lm = self.num_landmarks

            # compute innovation for each landmark
            for li in range(num_lm):
                lx = float(self.x.data[3 + 2*li][0])
                ly = float(self.x.data[3 + 2*li + 1][0])
                xr = float(self.x.data[0][0]); yr = float(self.x.data[1][0])
                dx = lx - xr; dy = ly - yr
                dist = math.hypot(dx, dy)
                if dist < 1e-6:
                    dist = 1e-6

                # build H row
                H = [0.0] * dim
                invd = 1.0 / dist
                H0 = -dx * invd; H1 = -dy * invd
                H[0] = H0; H[1] = H1; H[2] = 0.0
                idx = 3 + 2*li
                H[idx] = dx * invd; H[idx+1] = dy * invd

                # scalar Sval = H * P * H^T + R_range
                Sval = 0.0
                # compute row_sum = P * H^T for each row, reuse P_data
                # compute Sval = H dot (P * H^T)
                for i in range(dim):
                    row = P_data[i]
                    acc = 0.0
                    # inner loop unrolled-ish
                    for j in range(dim):
                        acc += row[j] * H[j]
                    Sval += H[i] * acc
                Sval += R_range

                y = r_meas - dist
                if Sval <= 0.0:
                    mahal = float('inf')
                else:
                    mahal = (y * y) / float(Sval)

                if mahal < best_mahal:
                    best_mahal = mahal
                    best_idx = li
                    best_H = H
                    best_Sval = Sval
                    best_dist = dist

            # gating / initialization logic
            if best_idx is None or best_mahal > gating_thresh:
                # if too many landmarks, avoid initializing further (simple cap)
                if self.num_landmarks >= self.max_landmarks:
                    # optionally prune oldest to make room
                    # here we skip initialization for speed; pruning can be enabled separately
                    continue
                self._initialize_landmark_from_range(r_meas, b, R_range)
                # prune if needed (simple oldest removal)
                if self.num_landmarks > self.max_landmarks:
                    self._prune_oldest(self.num_landmarks - self.max_landmarks)
                continue

            # standard EKF update using scalar math
            H_row = best_H
            Sval = best_Sval
            if Sval <= 0.0:
                continue

            # Kalman gain K = P * H^T / Sval
            K = [0.0] * dim
            for i in range(dim):
                row = P_data[i]
                s = 0.0
                for j in range(dim):
                    s += row[j] * H_row[j]
                K[i] = s / Sval

            y_scalar = r_meas - best_dist

            # state update
            for i in range(dim):
                self.x.data[i][0] += K[i] * y_scalar
            self.x.data[2][0] = wrap_angle(self.x.data[2][0])

            # covariance update P = P - K * H * P  (element-wise)
            Pnew = [[0.0] * dim for _ in range(dim)]
            # precompute H * P columns to reduce repeated work
            HP_cols = [[0.0]*dim for _ in range(dim)]
            for k in range(dim):
                hk = H_row[k]
                if hk == 0.0:
                    continue
                pk_row = P_data[k]
                for j in range(dim):
                    HP_cols[k][j] = hk * pk_row[j]

            for i in range(dim):
                Ki = K[i]
                row_i = P_data[i]
                new_row = Pnew[i]
                # Pnew_ij = P_ij - K[i] * sum_k H[k] * P[k][j]
                for j in range(dim):
                    s = 0.0
                    # sum over k
                    for k in range(dim):
                        s += HP_cols[k][j]
                    new_row[j] = row_i[j] - Ki * s

            self.P = Matrix(Shape(dim, dim), data=Pnew)

    def _initialize_landmark_from_range(self, r, bearing, R_range):
        xr = float(self.x.data[0][0]); yr = float(self.x.data[1][0]); th = float(self.x.data[2][0])
        phi = wrap_angle(th + bearing)
        lx = xr + r * math.cos(phi); ly = yr + r * math.sin(phi)

        old_n = self.dim
        new_state = [self.x.data[i][0] for i in range(old_n)] + [lx, ly]
        self.x = self._ensure_col(new_state)
        self.num_landmarks += 1

        J = [[1.0, 0.0, -r * math.sin(phi)],
             [0.0, 1.0,  r * math.cos(phi)]]

        new_n = old_n + 2
        Pnew = [[0.0]*new_n for _ in range(new_n)]
        # copy old P
        for i in range(old_n):
            rowi = self.P.data[i]
            for j in range(old_n):
                Pnew[i][j] = rowi[j]

        # compute P_xl = P_xx * J^T
        Jt = [[J[row][col] for row in range(2)] for col in range(3)]
        for i in range(old_n):
            for a in range(2):
                s = 0.0
                for k in range(3):
                    s += self.P.data[i][k] * Jt[k][a]
                Pnew[i][old_n + a] = s
                Pnew[old_n + a][i] = s

        # P_ll = J * P_xx * J^T + small_init
        temp = [[0.0]*old_n for _ in range(2)]
        for r0 in range(2):
            for c0 in range(old_n):
                s = 0.0
                for k in range(3):
                    s += J[r0][k] * self.P.data[k][c0]
                temp[r0][c0] = s
        for r0 in range(2):
            for c0 in range(2):
                s = 0.0
                for k in range(old_n):
                    s += temp[r0][k] * (Jt[k][c0] if k < 3 else 0.0)
                s += 1e-2 if r0 == c0 else 0.0
                Pnew[old_n + r0][old_n + c0] = s

        self.P = Matrix(Shape(new_n, new_n), data=Pnew)

    def _prune_oldest(self, count=1):
        """Remove `count` oldest landmarks (simple FIFO)."""
        count = int(max(1, count))
        for _ in range(count):
            if self.num_landmarks == 0:
                return
            old_n = self.dim
            # remove landmark index 0 (oldest)
            rem_idx = 3  # first landmark x index
            # build new state list skipping the two entries
            new_state = [self.x.data[i][0] for i in range(old_n) if i not in (rem_idx, rem_idx + 1)]
            new_n = old_n - 2
            # build new P by skipping rows/cols rem_idx and rem_idx+1
            Pnew = []
            for i in range(old_n):
                if i in (rem_idx, rem_idx + 1):
                    continue
                new_row = []
                for j in range(old_n):
                    if j in (rem_idx, rem_idx + 1):
                        continue
                    new_row.append(self.P.data[i][j])
                Pnew.append(new_row)
            self.x = self._ensure_col(new_state)
            self.P = Matrix(Shape(new_n, new_n), data=Pnew)
            self.num_landmarks -= 1

    def state(self):
        return [self.x.data[i][0] for i in range(self.dim)]

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

# -----------------------
# Environment raycast helpers
# -----------------------
def intersect_ray_segment(rx, ry, dx, dy, x1, y1, x2, y2):
    # ray: p = (rx,ry) + t*(dx,dy), t>=0
    # segment: s = (x1,y1) + u*(x2-x1, y2-y1), u in [0,1]
    sx = x2 - x1
    sy = y2 - y1
    denom = dx * sy - dy * sx
    if abs(denom) < 1e-9:
        return None
    t = ((x1 - rx) * sy - (y1 - ry) * sx) / denom
    u = ((x1 - rx) * dy - (y1 - ry) * dx) / denom
    if t >= 0 and 0.0 <= u <= 1.0:
        ix = rx + t * dx
        iy = ry + t * dy
        return math.hypot(ix - rx, iy - ry)
    return None

def raycast_walls(rx, ry, angle, walls, max_range=10.0):
    dx = math.cos(angle)
    dy = math.sin(angle)
    best = max_range
    for (x1,y1,x2,y2) in walls:
        res = intersect_ray_segment(rx, ry, dx, dy, x1, y1, x2, y2)
        if res is not None and res < best:
            best = res
    return best

# -----------------------
# Simulation
# -----------------------
def main():
    pygame.init()
    W, H = 1000, 800
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    scale = 60.0
    origin = (W//2, H//2)

    # environment: rectangle walls (clockwise)
    env = [(-4.0, -3.0, 4.0, -3.0),
           (4.0, -3.0, 4.0, 3.0),
           (4.0, 3.0, -4.0, 3.0),
           (-4.0, 3.0, -4.0, -3.0)]
    # additional internal wall (example)
    env.append((-1.0, -1.0, 2.5, -1.0))

    # robot true state
    rx, ry, rth = -2.0, 0.0, 0.0
    v_cmd = 0.6
    w_cmd = 0.2

    # sensors: four bearings (0,90,180,270 deg)
    base_bearings = [0.0, math.pi / 2.0, math.pi, -math.pi / 2.0]
    bearings = [wrap_angle(b + math.pi) for b in base_bearings]
    sensor_noise = 0.05  # range stddev
    R_range = sensor_noise**2

    # EKF-SLAM
    slam = EKFSLAM(Q=diag_matrix(3, 1e-4))
    # optionally pre-seed a landmark (none)
    running = True
    sim_dt = 1.0 / 30.0
    t = 0.0

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        # simple control profile
        rx += v_cmd * math.cos(rth) * sim_dt
        ry += v_cmd * math.sin(rth) * sim_dt
        rth = wrap_angle(rth + w_cmd * sim_dt)

        # generate noisy range measurements
        ranges = []
        for b in bearings:
            true_range = raycast_walls(rx, ry, rth + b, env, max_range=10.0)
            meas = true_range + random.gauss(0.0, sensor_noise)
            meas = max(0.0, min(10.0, meas))
            ranges.append(meas)

        # SLAM predict (use same motion as robot model)
        slam.predict(v_cmd, w_cmd, sim_dt)

        # update with all beams sequentially
        slam.update_ranges(ranges, bearings, R_range, gating_thresh=6.63)  # 1-DOF gate ~6.63 (looser)

        # draw
        screen.fill((30,30,30))
        # grid
        step = int(scale)
        for gx in range(0, W, step):
            pygame.draw.line(screen, (40,40,40), (gx, 0), (gx, H))
        for gy in range(0, H, step):
            pygame.draw.line(screen, (40,40,40), (0, gy), (W, gy))

        # draw walls
        for (x1,y1,x2,y2) in env:
            p1 = (origin[0] + x1*scale, origin[1] - y1*scale)
            p2 = (origin[0] + x2*scale, origin[1] - y2*scale)
            pygame.draw.line(screen, (200,200,200), p1, p2, 3)

        # draw robot true
        def draw_robot(surface, color, pose, size=8):
            x,y,theta = pose
            sx = origin[0] + x*scale
            sy = origin[1] - y*scale
            r = max(4, size)
            front = (sx + r*math.cos(theta), sy + r*math.sin(theta))
            left = (sx + r*math.cos(theta + 2.5), sy + r*math.sin(theta + 2.5))
            right = (sx + r*math.cos(theta - 2.5), sy + r*math.sin(theta - 2.5))
            pygame.draw.polygon(surface, color, [front, left, right])
        draw_robot(screen, (60,255,80), (rx, ry, rth), size=12)

        # draw sensor rays (true)
        for b, r in zip(bearings, ranges):
            angle = rth + b
            sx = origin[0] + rx*scale
            sy = origin[1] - ry*scale
            ex = sx + r*scale*math.cos(angle)
            ey = sy + r*scale*math.sin(angle)
            pygame.draw.line(screen, (255,120,60), (sx, sy), (ex, ey), 1)
            pygame.draw.circle(screen, (255,120,60), (int(ex), int(ey)), 3)

        # draw estimated robot (from SLAM)
        est = slam.state()
        ex_r = est[0]; ey_r = est[1]; eth_r = est[2]
        draw_robot(screen, (80,140,255), (ex_r, ey_r, eth_r), size=10)

        # draw landmarks
        for i in range(slam.num_landmarks):
            lx = slam.x.data[3 + 2*i][0]
            ly = slam.x.data[3 + 2*i + 1][0]
            px = origin[0] + lx*scale
            py = origin[1] - ly*scale
            pygame.draw.circle(screen, (255,200,60), (int(px), int(py)), 5)
            # draw covariance ellipse for landmark
            a = slam.P.data[3+2*i][3+2*i]
            b = slam.P.data[3+2*i][3+2*i+1] if 3+2*i+1 < slam.dim else 0.0
            c = slam.P.data[3+2*i+1][3+2*i] if 3+2*i+1 < slam.dim else 0.0
            d = slam.P.data[3+2*i+1][3+2*i+1] if 3+2*i+1 < slam.dim else 0.0
            cov = [[a, b], [c, d]]
            draw_cov_ellipse(screen, (int(px), int(py)), cov, scale, color=(255,200,60,60))

        # HUD
        hud_x = 10; hud_y = 10
        screen.blit(font.render(f"Landmarks = {slam.num_landmarks}", True, (220,220,220)), (hud_x, hud_y))
        screen.blit(font.render("Close window to exit", True, (180,180,180)), (hud_x, hud_y + 20))

        pygame.display.flip()
        clock.tick(30)
        t += sim_dt

    pygame.quit()

if __name__ == "__main__":
    main()
