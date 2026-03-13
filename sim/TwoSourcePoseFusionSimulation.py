# python
import math
import random
import pygame
from VEXLib.Math.Matrix import Matrix, Shape
from sim.ExtendedKalmanFilter import PoseEKF

# simple diagonal matrix helper
def diag_matrix(size, var):
    return Matrix(Shape(size, size),
                  data=[[var if i == j else 0.0 for j in range(size)] for i in range(size)])

def transpose(mat):
    rows = mat.shape.y_size
    cols = mat.shape.x_size
    transposed = [[mat.data[r][c] for r in range(rows)] for c in range(cols)]
    return Matrix(Shape(rows, cols), transposed)

# draw small triangle for pose
def draw_pose(surface, color, pose, scale, origin, size=8):
    x, y, theta = pose
    sx = origin[0] + x * scale
    sy = origin[1] - y * scale
    r = max(3, int(size * scale / 30.0))
    pts = [
        (sx + r * math.cos(theta), sy + r * math.sin(theta)),
        (sx + r * math.cos(theta + 2.5), sy + r * math.sin(theta + 2.5)),
        (sx + r * math.cos(theta - 2.5), sy + r * math.sin(theta - 2.5)),
    ]
    pygame.draw.polygon(surface, color, pts)

# draw circle for position-only sensors
def draw_pos_dot(surface, color, pos, scale, origin, radius=4):
    sx = origin[0] + pos[0] * scale
    sy = origin[1] - pos[1] * scale
    pygame.draw.circle(surface, color, (int(sx), int(sy)), max(2, int(radius * scale / 30.0)))

# small 2x2 eig / ellipse helper
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

def draw_cov_ellipse(surface, center_px, cov_2x2, scale, color=(80, 140, 255, 80)):
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

# generic linear EKF update helper (sequential fusion)
def ekf_linear_update(kf, H, z, R, angle_meas_indices=None):
    z_col = kf._ensure_col(z, expected_rows=H.shape.y_size)
    z_pred = H * kf.x
    y = z_col - z_pred
    if angle_meas_indices:
        for idx in angle_meas_indices:
            y.data[idx][0] = kf._wrap_angle(y.data[idx][0])
    S = (H * kf.P * kf._transpose(H)) + R
    try:
        S_inv = S.inverse()
        K = kf.P * kf._transpose(H) * S_inv
        kf.x = kf.x + (K * y)
        # wrap state angle (assume index 2)
        try:
            kf.x.data[2][0] = kf._wrap_angle(kf.x.data[2][0])
        except Exception:
            pass
        I = Matrix.identity(kf.n)
        kf.P = (I - (K * H)) * kf.P
        # NIS
        yT = kf._transpose(y)
        nis_mat = (yT * S_inv * y)
        nis = float(nis_mat.data[0][0])
    except Exception:
        nis = float('nan')
    return nis

def main():
    pygame.init()
    W, H = 2000, 2000
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 60)

    scale = 200.0
    origin = (W // 2, H // 2)

    # true pose and motion params
    true_pose = [0.0, 0.0, 0.0]
    vx, vy = 0.6, 0.2
    omega = 0.6

    # sensor specs
    # sensor A: position-only (GPS-like), lower rate
    sensorA_rate = 5.0  # Hz
    sensorA_dt = 1.0 / sensorA_rate
    measA_std_xy = 0.2

    # sensor B: full pose (x,y,theta), higher rate
    sensorB_rate = 15.0  # Hz
    sensorB_dt = 1.0 / sensorB_rate
    measB_std_xy = 0.12
    measB_std_theta = 0.08

    # EKF setup (uses PoseEKF: state [x,y,theta,v,omega])
    n = 5
    mA = 2
    mB = 3

    Q0 = diag_matrix(n, 1e-3)
    R_A0 = Matrix(Shape(mA, mA), data=[[measA_std_xy**2, 0.0], [0.0, measA_std_xy**2]])
    R_B0 = Matrix(Shape(mB, mB),
                  data=[[measB_std_xy**2, 0.0, 0.0],
                        [0.0, measB_std_xy**2, 0.0],
                        [0.0, 0.0, measB_std_theta**2]])
    P0 = diag_matrix(n, 1.0)

    v0 = math.hypot(vx, vy)
    w0 = omega
    kf = PoseEKF(Q=Q0, R=R_B0, P=P0, x0=[0.0, 0.0, 0.0, v0, w0])

    # H matrices
    H_A = Matrix(Shape(kf.n, mA), data=[
        [1.0, 0.0, 0.0, 0.0, 0.0],  # x
        [0.0, 1.0, 0.0, 0.0, 0.0],  # y
    ])
    H_B = Matrix(Shape(kf.n, mB), data=[
        [1.0, 0.0, 0.0, 0.0, 0.0],  # x
        [0.0, 1.0, 0.0, 0.0, 0.0],  # y
        [0.0, 0.0, 1.0, 0.0, 0.0],  # theta
    ])

    # scaling & NIS tracking
    Q_base = [Q0.data[i][i] for i in range(n)]
    R_A_base = [R_A0.data[i][i] for i in range(mA)]
    R_B_base = [R_B0.data[i][i] for i in range(mB)]
    q_scale = 1.0
    rA_scale = 1.0
    rB_scale = 1.0

    running = True
    sim_dt = 1.0 / 30.0
    t = 0.0

    ta_acc = 0.0
    tb_acc = 0.0

    nisA_hist = []
    nisB_hist = []
    nis_window = 50
    last_nisA = float('nan')
    last_nisB = float('nan')

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    q_scale *= 2.0
                elif ev.key == pygame.K_a:
                    q_scale = max(1e-6, q_scale * 0.5)
                elif ev.key == pygame.K_w:
                    rA_scale *= 2.0
                elif ev.key == pygame.K_s:
                    rA_scale = max(1e-6, rA_scale * 0.5)
                elif ev.key == pygame.K_e:
                    rB_scale *= 2.0
                elif ev.key == pygame.K_d:
                    rB_scale = max(1e-6, rB_scale * 0.5)
                elif ev.key == pygame.K_r:
                    q_scale = 1.0; rA_scale = 1.0; rB_scale = 1.0
                    kf.P = P0

                # apply Q/R scaling
                for i in range(n):
                    kf.Q.data[i][i] = Q_base[i] * q_scale
                for i in range(mA):
                    R_A0.data[i][i] = R_A_base[i] * rA_scale
                for i in range(mB):
                    R_B0.data[i][i] = R_B_base[i] * rB_scale
                # keep kf.R in a sensible default for PoseEKF (we'll use R_B0 for full-pose updates)
                kf.R = R_B0

        # advance true pose
        true_pose[0] += vx * sim_dt * math.cos(0.2 * t) - vy * sim_dt * math.sin(0.1 * t)
        true_pose[1] += vx * sim_dt * math.sin(0.2 * t) + vy * sim_dt * math.cos(0.1 * t)
        true_pose[2] += omega * sim_dt * 0.6

        # noisy measurements (always available but applied according to sensor rates)
        measA_x = true_pose[0] + random.gauss(0.0, measA_std_xy)
        measA_y = true_pose[1] + random.gauss(0.0, measA_std_xy)

        measB_x = true_pose[0] + random.gauss(0.0, measB_std_xy)
        measB_y = true_pose[1] + random.gauss(0.0, measB_std_xy)
        measB_theta = true_pose[2] + random.gauss(0.0, measB_std_theta)

        # Predict step (EKF)
        kf.predict(sim_dt)

        # accumulate time and trigger sensor updates when due
        ta_acc += sim_dt
        tb_acc += sim_dt

        if ta_acc >= sensorA_dt:
            # apply sensor A (pos-only)
            R_A = Matrix(Shape(mA, mA), data=[[R_A0.data[0][0], 0.0], [0.0, R_A0.data[1][1]]])
            last_nisA = ekf_linear_update(kf, H_A, [measA_x, measA_y], R_A, angle_meas_indices=None)
            if not math.isnan(last_nisA):
                nisA_hist.append(last_nisA)
                if len(nisA_hist) > nis_window:
                    nisA_hist.pop(0)
            ta_acc -= sensorA_dt

        if tb_acc >= sensorB_dt:
            # apply sensor B (full pose)
            R_B = Matrix(Shape(mB, mB), data=[
                [R_B0.data[0][0], 0.0, 0.0],
                [0.0, R_B0.data[1][1], 0.0],
                [0.0, 0.0, R_B0.data[2][2]],
            ])
            last_nisB = ekf_linear_update(kf, H_B, [measB_x, measB_y, measB_theta], R_B, angle_meas_indices=[2])
            if not math.isnan(last_nisB):
                nisB_hist.append(last_nisB)
                if len(nisB_hist) > nis_window:
                    nisB_hist.pop(0)
            tb_acc -= sensorB_dt

        nisA_avg = sum(nisA_hist) / len(nisA_hist) if nisA_hist else 0.0
        nisB_avg = sum(nisB_hist) / len(nisB_hist) if nisB_hist else 0.0

        est = [kf.x.data[i][0] for i in range(3)]

        # draw
        screen.fill((30, 30, 30))
        step = max(1, int(scale))
        for gx in range(0, W, step):
            pygame.draw.line(screen, (40, 40, 40), (gx, 0), (gx, H))
        for gy in range(0, H, step):
            pygame.draw.line(screen, (40, 40, 40), (0, gy), (W, gy))

        # draw measurements and states
        draw_pos_dot(screen, (255, 120, 60), (measA_x, measA_y), scale, origin, radius=5)  # sensor A (orange)
        draw_pose(screen, (200, 60, 200), (measB_x, measB_y, measB_theta), scale, origin, size=6)  # sensor B (magenta)
        draw_pose(screen, (60, 255, 80), tuple(true_pose), scale, origin, size=10)  # true (green)
        draw_pose(screen, (80, 140, 255), tuple(est), scale, origin, size=9)  # estimate (blue)

        # covariance ellipse
        Ppos = [[kf.P.data[0][0], kf.P.data[0][1]],
                [kf.P.data[1][0], kf.P.data[1][1]]]
        center_px = (int(origin[0] + est[0] * scale), int(origin[1] - est[1] * scale))
        draw_cov_ellipse(screen, center_px, Ppos, scale, color=(80, 140, 255, 60))

        # HUD
        hud_x = 10; hud_y = 10
        screen.blit(font.render(f"Q scale (q/a) = {q_scale:.6g}", True, (220, 220, 220)), (hud_x, hud_y))
        screen.blit(font.render(f"R_A scale (w/s) = {rA_scale:.6g}", True, (220, 220, 220)), (hud_x, hud_y + 60))
        screen.blit(font.render(f"R_B scale (e/d) = {rB_scale:.6g}", True, (220, 220, 220)), (hud_x, hud_y + 120))
        screen.blit(font.render(f"SensorA rate = {sensorA_rate:.1f} Hz  SensorB rate = {sensorB_rate:.1f} Hz", True, (180, 180, 180)), (hud_x, hud_y + 200))
        screen.blit(font.render(f"NIS A last/avg = {last_nisA:.3f} / {nisA_avg:.3f}", True, (220, 220, 220)), (hud_x, hud_y + 260))
        screen.blit(font.render(f"NIS B last/avg = {last_nisB:.3f} / {nisB_avg:.3f}", True, (220, 220, 220)), (hud_x, hud_y + 320))
        screen.blit(font.render("q/a = scale Q, w/s = scale R_A, e/d = scale R_B, r = reset", True, (180, 180, 180)), (hud_x, hud_y + 380))

        pygame.display.flip()
        clock.tick(15)
        t += sim_dt

    pygame.quit()

if __name__ == "__main__":
    main()