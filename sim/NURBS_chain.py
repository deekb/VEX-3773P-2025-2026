from sim.splines import NURBS, CompositeCurve, BSpline, Curve, Bezier
import math

CURVE_TYPES = [Bezier, BSpline, NURBS]
CURVE_TYPE_NAMES = {Bezier: "Bezier", BSpline: "BSpline", NURBS: "NURBS"}

def make_curve(curve_type, pts, weights=None, degree=2):
    if curve_type is NURBS:
        return NURBS(pts, weights, degree)
    elif curve_type is BSpline:
        return BSpline(pts, degree)
    elif curve_type is Bezier:
        return Bezier(pts)
    else:
        raise ValueError("Unsupported curve type")

def draw_curvature_comb(crv, to_screen, screen, steps=200, scale=80):
    pts = crv.sample(steps)
    tangents = [crv.derivative(t) for t in [i/(steps-1) for i in range(steps)]]
    d2s = [crv.second_derivative(t) for t in [i/(steps-1) for i in range(steps)]]
    comb_ends = []
    for i, (p, d1, d2) in enumerate(zip(pts, tangents, d2s)):
        dx, dy = d1
        ddx, ddy = d2
        denom = (dx*dx + dy*dy)**1.5
        if denom == 0:
            continue
        kappa = (dx*ddy - dy*ddx) / denom
        nx, ny = -dy, dx
        norm = math.hypot(nx, ny)
        if norm == 0:
            continue
        nx, ny = nx / norm, ny / norm
        comb_len = kappa * scale
        x0, y0 = to_screen(p)
        x1, y1 = int(x0 + nx * comb_len), int(y0 + ny * comb_len)
        import pygame
        pygame.draw.line(screen, (0, 200, 255), (x0, y0), (x1, y1), 2)
        comb_ends.append((x1, y1))
    import pygame
    for i in range(len(comb_ends) - 1):
        pygame.draw.line(screen, (255, 100, 0), comb_ends[i], comb_ends[i + 1], 1)

def pygame_nurbs_chain_demo():
    try:
        import pygame
    except Exception as e:
        print("pygame is required for pygame_nurbs_chain_demo()", e)
        return

    pygame.init()
    W, H = 2000, 1200
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    nurbs_pts = [
        [(80, 300), (140, 200), (200, 400), (260, 300)],
        [(260, 300), (320, 200), (380, 400), (440, 300)],
        [(440, 300), (500, 200), (560, 400), (620, 300)],
        [(620, 300), (680, 200), (740, 400), (800, 300)],
        [(800, 300), (860, 200), (920, 400), (980, 300)],
    ]
    nurbs_weights = [
        [1.0, 2.0, 1.0, 1.0],
        [1.0, 1.5, 2.0, 1.0],
        [1.0, 2.0, 1.0, 1.0],
        [1.0, 1.5, 2.0, 1.0],
        [1.0, 2.0, 1.0, 1.0],
    ]
    degree = 2

    current_curve_type = BSpline

    def build_curve_list():
        curves = []
        for i, pts in enumerate(nurbs_pts):
            if current_curve_type is NURBS:
                curves.append(make_curve(NURBS, pts, nurbs_weights[i], degree))
            elif current_curve_type is BSpline:
                curves.append(make_curve(BSpline, pts, degree=degree))
            elif current_curve_type is Bezier:
                curves.append(make_curve(Bezier, pts))
        return curves

    nurbs_list = build_curve_list()
    composite = CompositeCurve(nurbs_list)

    selected = None
    ui_scale = 2.0
    ui_offset = [0, 0]

    def to_screen(pt):
        return int(pt[0] * ui_scale + ui_offset[0]), int(pt[1] * ui_scale + ui_offset[1])

    def from_screen(pt):
        return (pt[0] - ui_offset[0]) / ui_scale, (pt[1] - ui_offset[1]) / ui_scale

    def draw_curve(crv, steps=200):
        pts = crv.sample(steps)
        import pygame as pg
        for i in range(len(pts) - 1):
            pg.draw.line(screen, (255, 255, 255), to_screen(pts[i]), to_screen(pts[i + 1]), 2)

    def draw_control():
        for seg_idx, pts in enumerate(nurbs_pts):
            for pt_idx, p in enumerate(pts):
                color = (200, 0, 200) if (seg_idx, pt_idx) == selected else (200, 200, 0)
                pygame.draw.circle(screen, color, to_screen(p), int(6 * ui_scale))

    def set_C1_at_joint(seg_idx, pt_idx):
        if pt_idx == 0 and seg_idx > 0:
            p_joint = nurbs_pts[seg_idx][0]
            p_prev = nurbs_pts[seg_idx - 1][-2]
            nurbs_pts[seg_idx - 1][-1] = p_joint
            nurbs_pts[seg_idx][1] = (
                2 * p_joint[0] - p_prev[0],
                2 * p_joint[1] - p_prev[1]
            )
        if pt_idx == len(nurbs_pts[seg_idx]) - 1 and seg_idx < len(nurbs_pts) - 1:
            p_joint = nurbs_pts[seg_idx][-1]
            p_next = nurbs_pts[seg_idx + 1][1]
            nurbs_pts[seg_idx + 1][0] = p_joint
            nurbs_pts[seg_idx][-2] = (
                2 * p_joint[0] - p_next[0],
                2 * p_joint[1] - p_next[1]
            )

    def set_C1_adjacent(seg_idx, pt_idx):
        if pt_idx == 1 and seg_idx > 0:
            p_joint = nurbs_pts[seg_idx][0]
            p_adj = nurbs_pts[seg_idx][1]
            nurbs_pts[seg_idx - 1][-2] = (
                2 * p_joint[0] - p_adj[0],
                2 * p_joint[1] - p_adj[1]
            )
        if pt_idx == len(nurbs_pts[seg_idx]) - 2 and seg_idx < len(nurbs_pts) - 1:
            p_joint = nurbs_pts[seg_idx][-1]
            p_adj = nurbs_pts[seg_idx][-2]
            nurbs_pts[seg_idx + 1][1] = (
                2 * p_joint[0] - p_adj[0],
                2 * p_joint[1] - p_adj[1]
            )

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    ui_scale *= 1.1
                elif ev.key in (pygame.K_MINUS, pygame.K_UNDERSCORE, pygame.K_KP_MINUS):
                    ui_scale /= 1.1
                elif ev.key == pygame.K_b:
                    current_curve_type = Bezier
                elif ev.key == pygame.K_s:
                    current_curve_type = BSpline
                elif ev.key == pygame.K_n:
                    current_curve_type = NURBS
                if ev.key in (pygame.K_b, pygame.K_s, pygame.K_n):
                    nurbs_list[:] = build_curve_list()
                    composite.curves = nurbs_list
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                for seg_idx, pts in enumerate(nurbs_pts):
                    for pt_idx, p in enumerate(pts):
                        sx, sy = to_screen(p)
                        if (sx - mx) ** 2 + (sy - my) ** 2 < (12 * ui_scale) ** 2:
                            selected = (seg_idx, pt_idx)
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                selected = None
            elif ev.type == pygame.MOUSEMOTION and selected is not None:
                mx, my = ev.pos
                seg_idx, pt_idx = selected
                nurbs_pts[seg_idx][pt_idx] = from_screen((mx, my))
                set_C1_at_joint(seg_idx, pt_idx)
                set_C1_adjacent(seg_idx, pt_idx)
                for i, nur in enumerate(nurbs_list):
                    nur.control = [tuple(p) for p in nurbs_pts[i]]

        screen.fill((20, 30, 40))
        draw_curve(composite)
        draw_curvature_comb(composite, to_screen, screen, scale=10000 / ui_scale)
        draw_control()
        font = pygame.font.SysFont(None, 20)
        txt = font.render(
            f"Drag control points. +/- to zoom. B/S/N to switch type. Endpoints are locked for C1 continuity. "
            f"Type: {CURVE_TYPE_NAMES[current_curve_type]}. Scale: {ui_scale:.2f}",
            True, (220, 220, 220)
        )
        screen.blit(txt, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    pygame_nurbs_chain_demo()