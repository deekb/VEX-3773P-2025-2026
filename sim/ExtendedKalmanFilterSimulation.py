# python
import math
import random
import pygame
from VEXLib.Math.Matrix import Matrix, Shape
from sim.ExtendedKalmanFilter import PoseEKF

# --- helper: build diagonal matrix ---
def diag_matrix(size, var):
    return Matrix(Shape(size, size),
                  data=[[var if i == j else 0.0 for j in range(size)] for i in range(size)])

def transpose(mat):
    rows = mat.shape.y_size
    cols = mat.shape.x_size
    transposed = [[mat.data[r][c] for r in range(rows)] for c in range(cols)]
    return Matrix(Shape(rows, cols), transposed)

# --- compute eigen-decomposition of 2x2 symmetric matrix ---
def eig2(a, b, c, d):
    tr = a + d
    det = a * d - b * c
    mid = tr * 0.5
    disc = max(0.0, mid * mid - det)
    s = math.sqrt(disc)
    l1 = mid + s
    l2 = mid - s
    # eigenvector for l1
    if abs(b) > 1e-12 or abs(a - l1) > 1e-12:
        v1 = (b, l1 - a)
    else:
        v1 = (l1 - d, c)
    mag = math.hypot(v1[0], v1[1])
    if mag <= 1e-12:
        v1 = (1.0, 0.0)
        mag = 1.0
    v1 = (v1[0] / mag, v1[1] / mag)
    # orthogonal vec
    v2 = (-v1[1], v1[0])
    return (l1, l2, v1, v2)

# --- draw a pose as a triangle ---
def draw_pose(surface, color, pose, scale, origin):
    x, y, theta = pose
    sx = origin[0] + x * scale
    sy = origin[1] - y * scale
    # scale triangle size with the visual scale
    r = max(4, int(8 * scale / 30.0))
    front = (sx + r * math.cos(theta), sy + r * math.sin(theta))
    left = (sx + r * math.cos(theta + 2.5), sy + r * math.sin(theta + 2.5))
    right = (sx + r * math.cos(theta - 2.5), sy + r * math.sin(theta - 2.5))
    pygame.draw.polygon(surface, color, [front, left, right])

# --- draw rotated covariance ellipse for position (2D) ---
def draw_cov_ellipse(surface, center_px, cov_2x2, scale, color=(80, 140, 255, 80)):
    # cov_2x2: [[a,b],[c,d]] (symmetric)
    a = cov_2x2[0][0]
    b = cov_2x2[0][1]
    c = cov_2x2[1][0]
    d = cov_2x2[1][1]
    l1, l2, v1, v2 = eig2(a, b, c, d)
    # 95% chi-square for 2 DOF
    chi2_95 = 5.991
    r1 = math.sqrt(max(0.0, l1 * chi2_95)) * scale
    r2 = math.sqrt(max(0.0, l2 * chi2_95)) * scale
    # surface size
    w = max(2, int(2 * r1))
    h = max(2, int(2 * r2))
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, color, (0, 0, w - 1, h - 1))
    # compute rotation angle from major axis vector v1
    angle = math.degrees(math.atan2(v1[1], v1[0]))
    rot = pygame.transform.rotate(surf, -angle)
    rect = rot.get_rect(center=center_px)
    surface.blit(rot, rect)

# --- main simulation ---
def main():
    pygame.init()
    W, H = 1200, 1200
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    # visual scale (doubled)
    scale = 60.0
    origin = (W // 2, H // 2)

    # True state: [x, y, theta]
    true_pose = [0.0, 0.0, 0.0]
    vx, vy = 0.6, 0.2
    omega = 0.6  # rad/s

    # measurement noise stddev (base values)
    meas_std_x = 0.3
    meas_std_y = 0.3
    meas_std_theta = 0.3

    # EKF filter setup (5 state dims, 3 measurement dims)
    n = 5
    m = 3

    # process noise for full state (small)
    Q0 = diag_matrix(n, 1e-3)
    # measurement covariance (x,y,theta)
    R0 = Matrix(Shape(m, m),
               data=[[meas_std_x**2, 0.0, 0.0],
                     [0.0, meas_std_y**2, 0.0],
                     [0.0, 0.0, meas_std_theta**2]])
    P0 = diag_matrix(n, 1.0)

    # initial velocity/omega guess
    v0 = math.hypot(vx, vy)
    w0 = omega

    kf = PoseEKF(Q=Q0, R=R0, P=P0, x0=[0.0, 0.0, 0.0, v0, w0])

    # keep base diagonal values so scaling updates are simple
    Q_base = [Q0.data[i][i] for i in range(n)]
    R_base = [R0.data[i][i] for i in range(m)]
    q_scale = 1.0
    r_scale = 1.0

    running = True
    dt = 1.0 / 30.0
    t = 0.0

    # NIS running average
    nis_history = []
    nis_window = 50

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                # process noise scale q/a
                if ev.key == pygame.K_q:
                    q_scale *= 2.0
                elif ev.key == pygame.K_a:
                    q_scale = max(1e-6, q_scale * 0.5)
                # measurement noise scale w/s
                elif ev.key == pygame.K_w:
                    r_scale *= 2.0
                elif ev.key == pygame.K_s:
                    r_scale = max(1e-6, r_scale * 0.5)
                # reset
                elif ev.key == pygame.K_r:
                    q_scale = 1.0
                    r_scale = 1.0
                    kf.P = P0

                # update Q and R matrices in filter
                for i in range(n):
                    kf.Q.data[i][i] = Q_base[i] * q_scale
                for i in range(m):
                    kf.R.data[i][i] = R_base[i] * r_scale

        # advance true pose
        true_pose[0] += vx * dt * math.cos(0.2 * t) - vy * dt * math.sin(0.1 * t)
        true_pose[1] += vx * dt * math.sin(0.2 * t) + vy * dt * math.cos(0.1 * t)
        true_pose[2] += omega * dt * 0.6

        # generate noisy measurement
        meas_x = true_pose[0] + random.gauss(0.0, meas_std_x)
        meas_y = true_pose[1] + random.gauss(0.0, meas_std_y)
        meas_theta = true_pose[2] + random.gauss(0.0, meas_std_theta)
        z_col = Matrix(Shape(1, m), data=[[meas_x], [meas_y], [meas_theta]])

        # Predict (EKF requires dt)
        kf.predict(dt)

        # compute innovation and S (prior) for NIS before calling update
        pred_meas = kf.H * kf.x  # column
        y = z_col - pred_meas
        S = (kf.H * kf.P * transpose(kf.H)) + kf.R
        try:
            S_inv = S.inverse()
            yT = transpose(y)
            nis_mat = (yT * S_inv * y)
            nis = float(nis_mat.data[0][0])
        except Exception:
            nis = float('nan')

        # Update (EKF expects list or Matrix)
        kf.update([meas_x, meas_y, meas_theta])
        est_full = kf.state()   # [x,y,theta,v,omega]
        est = est_full[0:3]

        # keep short running history
        if not math.isnan(nis):
            nis_history.append(nis)
            if len(nis_history) > nis_window:
                nis_history.pop(0)
        nis_avg = sum(nis_history) / len(nis_history) if nis_history else 0.0

        # draw
        screen.fill((30, 30, 30))
        step = max(1, int(scale))
        for gx in range(0, W, step):
            pygame.draw.line(screen, (40, 40, 40), (gx, 0), (gx, H))
        for gy in range(0, H, step):
            pygame.draw.line(screen, (40, 40, 40), (0, gy), (W, gy))

        # measurement (red), true (green), estimate (blue)
        draw_pose(screen, (255, 60, 60), (meas_x, meas_y, meas_theta), scale, origin)
        draw_pose(screen, (60, 255, 80), tuple(true_pose), scale, origin)
        draw_pose(screen, (80, 140, 255), tuple(est), scale, origin)

        # draw covariance ellipse from kf.P top-left 2x2
        Ppos = [[kf.P.data[0][0], kf.P.data[0][1]],
                [kf.P.data[1][0], kf.P.data[1][1]]]
        center_px = (int(origin[0] + est[0] * scale), int(origin[1] - est[1] * scale))
        draw_cov_ellipse(screen, center_px, Ppos, scale, color=(80, 140, 255, 80))

        # HUD
        hud_x = 10
        hud_y = 10
        screen.blit(font.render(f"Q scale (q/a) = {q_scale:.6g}", True, (220, 220, 220)), (hud_x, hud_y))
        screen.blit(font.render(f"R scale (w/s) = {r_scale:.6g}", True, (220, 220, 220)), (hud_x, hud_y + 20))
        screen.blit(font.render(f"NIS latest = {nis:.3f}", True, (220, 220, 220)), (hud_x, hud_y + 40))
        screen.blit(font.render(f"NIS avg ({len(nis_history)}) = {nis_avg:.3f}", True, (220, 220, 220)), (hud_x, hud_y + 60))
        screen.blit(font.render("r = reset scales and P", True, (180, 180, 180)), (hud_x, hud_y + 90))

        pygame.display.flip()
        clock.tick(30)
        t += dt

    pygame.quit()

if __name__ == "__main__":
    main()