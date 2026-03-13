"""
splines.py

A small class-based modular spline engine supporting:
 - Bezier (de Casteljau)
 - B-Spline (Cox-de Boor)
 - NURBS (rational B-spline)
 - CompositeCurve (join multiple curves)
Includes a pygame_demo() for local interactive testing.

Author: Derek Baier
"""

def linear_interpolate(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


class Curve:
    """Abstract interface"""

    def evaluate(self, t):
        raise NotImplementedError

    def sample(self, n):
        if n < 2:
            return [self.evaluate(0.0)]
        return [self.evaluate(i / (n - 1)) for i in range(n)]

    def derivative(self, t):
        raise NotImplementedError

    def second_derivative(self, t):
        raise NotImplementedError


# -----------------------
# Bezier
# -----------------------
class Bezier(Curve):
    def __init__(self, control):
        assert len(control) >= 2, "Bezier needs at least 2 control points"
        self.control = [tuple(p) for p in control]
        self.degree = len(control) - 1

    def evaluate(self, t):
        # de Casteljau iterative
        pts = [p for p in self.control]
        n = len(pts)
        for r in range(1, n):
            for i in range(n - r):
                pts[i] = linear_interpolate(pts[i], pts[i + 1], t)
        return pts[0]

    def derivative(self, t):
        n = self.degree
        if n == 0:
            return 0.0, 0.0
        dpts = [
            (n * (b[0] - a[0]), n * (b[1] - a[1]))
            for a, b in zip(self.control[:-1], self.control[1:])
        ]
        # Evaluate derivative as a Bezier curve of degree n-1
        if len(dpts) == 1:
            return dpts[0]
        pts = [p for p in dpts]
        for r in range(1, len(pts)):
            for i in range(len(pts) - r):
                pts[i] = linear_interpolate(pts[i], pts[i + 1], t)
        return pts[0]

    def second_derivative(self, t):
        n = self.degree
        if n < 2:
            return 0.0, 0.0
        d2pts = [
            ((n - 1) * (b[0] - a[0]), (n - 1) * (b[1] - a[1]))
            for a, b in zip(self.control[:-1], self.control[1:])
        ]
        d2 = Bezier(d2pts).derivative(t)
        return d2


# -----------------------
# B-Spline - Cox-de Boor basis
# -----------------------
def cox_de_boor(u, i, k, knot):
    """Return basis function N_{i,k}(u), where k = order (degree+1)."""
    if k == 1:
        # N_{i,1}(u)
        left = knot[i]
        right = knot[i + 1]
        # canonical half-open interval, include last knot endpoint only for the final span
        if left <= u < right:
            return 1.0
        if u == knot[-1] and right == knot[-1] and left <= u <= right:
            return 1.0
        return 0.0
    denom1 = knot[i + k - 1] - knot[i]
    denom2 = knot[i + k] - knot[i + 1]
    term1 = 0.0
    term2 = 0.0
    if denom1 != 0:
        term1 = (u - knot[i]) / denom1 * cox_de_boor(u, i, k - 1, knot)
    if denom2 != 0:
        term2 = (knot[i + k] - u) / denom2 * cox_de_boor(u, i + 1, k - 1, knot)
    return term1 + term2


class BSpline(Curve):
    def __init__(self, control, degree, knot=None):
        assert degree >= 1, "degree must be >= 1"
        assert len(control) >= degree + 1, "need at least degree+1 control points"
        self.control = [tuple(p) for p in control]
        self.degree = degree
        self.order = degree + 1
        n = len(control)
        if knot is None:
            # build a clamped uniform knot vector
            m = n + self.order  # m = n + k
            internal_count = m - 2 * self.order
            knot = []
            knot += [0.0] * self.order
            if internal_count > 0:
                for j in range(1, internal_count + 1):
                    knot.append(j / (internal_count + 1))
            knot += [1.0] * self.order
        assert len(knot) == len(control) + self.order, "knot vector size mismatch"
        self.knot = list(knot)

    def evaluate(self, t):
        # map t in [0,1] to knot domain [knot[order-1], knot[-order]]
        u_min = self.knot[self.order - 1]
        u_max = self.knot[-self.order]
        u = u_min + (u_max - u_min) * t
        x = 0.0
        y = 0.0
        for i, P in enumerate(self.control):
            N = cox_de_boor(u, i, self.order, self.knot)
            x += N * P[0]
            y += N * P[1]
        return x, y

    def derivative(self, t):
        # Numerical finite difference
        eps = 1e-5
        p1 = self.evaluate(max(0.0, t - eps))
        p2 = self.evaluate(min(1.0, t + eps))
        return (p2[0] - p1[0]) / (2 * eps), (p2[1] - p1[1]) / (2 * eps)

    def second_derivative(self, t):
        eps = 1e-5
        p0 = self.evaluate(max(0.0, t - eps))
        p1 = self.evaluate(t)
        p2 = self.evaluate(min(1.0, t + eps))
        return (
            (p2[0] - 2 * p1[0] + p0[0]) / (eps**2),
            (p2[1] - 2 * p1[1] + p0[1]) / (eps**2),
        )


# -----------------------
# NURBS (rational)
# -----------------------
class NURBS(Curve):
    def __init__(self, control, weights, degree, knot=None):
        assert len(control) == len(weights), "control and weights must match"
        self.control = [tuple(p) for p in control]
        self.weights = list(weights)
        self.degree = degree
        self.order = degree + 1
        # reuse BSpline knot construction (clamped uniform) if knot is None
        temp = BSpline(control, degree, knot)
        self.knot = temp.knot

    def evaluate(self, t):
        u_min = self.knot[self.order - 1]
        u_max = self.knot[-self.order]
        u = u_min + (u_max - u_min) * t
        num_x = 0.0
        num_y = 0.0
        den = 0.0
        for i, P in enumerate(self.control):
            N = cox_de_boor(u, i, self.order, self.knot)
            wN = self.weights[i] * N
            num_x += wN * P[0]
            num_y += wN * P[1]
            den += wN
        if den == 0:
            return 0.0, 0.0
        return num_x / den, num_y / den

    derivative = BSpline.derivative
    second_derivative = BSpline.second_derivative


# -----------------------
# Composite / joining curves
# -----------------------
class CompositeCurve(Curve):
    def __init__(self, curves, param_lengths=None):
        assert len(curves) >= 1
        self.curves = curves
        if param_lengths is None:
            self.param_lengths = [1.0 / len(curves)] * len(curves)
        else:
            assert len(param_lengths) == len(curves)
            s = sum(param_lengths)
            self.param_lengths = [pl / s for pl in param_lengths]

    def evaluate(self, t):
        if t <= 0:
            return self.curves[0].evaluate(0.0)
        if t >= 1:
            return self.curves[-1].evaluate(1.0)
        acc = 0.0
        for i, frac in enumerate(self.param_lengths):
            if acc + frac >= t:
                local_t = (t - acc) / frac if frac > 0 else 0.0
                return self.curves[i].evaluate(local_t)
            acc += frac
        return self.curves[-1].evaluate(1.0)

    def derivative(self, t):
        if t <= 0:
            return self.curves[0].derivative(0.0)
        if t >= 1:
            return self.curves[-1].derivative(1.0)
        acc = 0.0
        for i, frac in enumerate(self.param_lengths):
            if acc + frac >= t:
                local_t = (t - acc) / frac if frac > 0 else 0.0
                return self.curves[i].derivative(local_t)
            acc += frac
        return self.curves[-1].derivative(1.0)

    def second_derivative(self, t):
        if t <= 0:
            return self.curves[0].second_derivative(0.0)
        if t >= 1:
            return self.curves[-1].second_derivative(1.0)
        acc = 0.0
        for i, frac in enumerate(self.param_lengths):
            if acc + frac >= t:
                local_t = (t - acc) / frac if frac > 0 else 0.0
                return self.curves[i].second_derivative(local_t)
            acc += frac
        return self.curves[-1].second_derivative(1.0)


def join_curves_c0(curve_a, curve_b):
    return CompositeCurve([curve_a, curve_b])


def make_open_uniform_bspline_from_bezier_segments(bezier_segments):
    """
    Simple helper that concatenates Bezier control polygons to form
    an approximate open uniform B-spline control polygon. This is an
    approximation; exact conversions require knot insertion algorithms.
    """
    if not bezier_segments:
        raise ValueError("no segments")
    degree = bezier_segments[0].degree
    for seg in bezier_segments:
        if seg.degree != degree:
            raise ValueError("all segments must have same degree for this helper")
    pts = []
    for i, seg in enumerate(bezier_segments):
        if i == 0:
            pts.extend(seg.control)
        else:
            pts.extend(seg.control[1:])
    return BSpline(pts, degree)


# -----------------------
# Optional: simple pygame demo
# -----------------------
def pygame_demo():
    """
    Interactive demo using pygame: drag control points (left click + drag)
    to see Bezier / BSpline / NURBS updates live. This function is intentionally
    minimal and for local use only.

    Usage:
        pip install pygame
        python -c "import splines; splines.pygame_demo()"
    """
    try:
        import pygame
    except Exception as e:
        print("pygame is required for pygame_demo()", e)
        return

    pygame.init()
    W, H = 900, 600
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    # Example curve sets
    bezier_pts = [(60, 300), (160, 80), (300, 520), (420, 300)]
    bs_pts = [(480, 120), (540, 300), (600, 200), (660, 500), (720, 240)]
    nurbs_pts = [(80, 480), (160, 450), (240, 500), (320, 420)]
    nurbs_weights = [1.0, 2.5, 0.8, 1.2]

    bez = Bezier(bezier_pts)
    bs = BSpline(bs_pts, degree=2)
    nur = NURBS(nurbs_pts, nurbs_weights, degree=2)

    selected = None
    selected_data = None  # tuple (which_list, index)

    def draw_curve(crv, steps=120):
        pts = crv.sample(steps)
        import pygame as pg
        for i in range(len(pts) - 1):
            pg.draw.line(screen, (255, 255, 255), pts[i], pts[i + 1], 2)

    def draw_control(pts):
        for p in pts:
            pygame.draw.circle(screen, (200, 200, 0), (int(p[0]), int(p[1])), 6)

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                # check control points proximity
                def find_near(pts):
                    for i, p in enumerate(pts):
                        if (p[0] - mx) ** 2 + (p[1] - my) ** 2 < 12 ** 2:
                            return i
                    return None

                idx = find_near(bezier_pts)
                if idx is not None:
                    selected = bezier_pts
                    selected_data = ("bezier", idx)
                else:
                    idx = find_near(bs_pts)
                    if idx is not None:
                        selected = bs_pts
                        selected_data = ("bs", idx)
                    else:
                        idx = find_near(nurbs_pts)
                        if idx is not None:
                            selected = nurbs_pts
                            selected_data = ("nurbs", idx)
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                selected = None
                selected_data = None
            elif ev.type == pygame.MOUSEMOTION and selected is not None:
                mx, my = ev.pos
                idx = selected_data[1]
                selected[idx] = (mx, my)
                # update curve objects
                bez.control = [tuple(p) for p in bezier_pts]
                bs.control = [tuple(p) for p in bs_pts]
                nur.control = [tuple(p) for p in nurbs_pts]

        screen.fill((20, 30, 40))

        # draw each curve
        draw_curve(bez)
        draw_control(bezier_pts)

        draw_curve(bs)
        draw_control(bs_pts)

        draw_curve(nur)
        draw_control(nurbs_pts)

        # small legend
        font = pygame.font.SysFont(None, 20)
        txt = font.render("Drag points with left mouse. Close window to exit.", True, (220, 220, 220))
        screen.blit(txt, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    pygame_demo()