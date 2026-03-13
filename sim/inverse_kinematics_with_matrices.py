"""
Stable 2D IK demo using Jacobian Transpose and a custom Matrix library
"""

import math
import pygame
import sys
import random
from dataclasses import dataclass

# -------------------------
# Minimal Shape + Matrix
# -------------------------
@dataclass
class Shape:
    x_size: int
    y_size: int


class Matrix:
    def __init__(self, shape: Shape, data=None):
        if shape.x_size <= 0 or shape.y_size <= 0:
            raise ValueError("Minimum matrix size is 1x1")
        self.shape = shape
        if data is None:
            self.data = [[0.0 for _ in range(shape.x_size)] for _ in range(shape.y_size)]
        else:
            self.data = [row[:] for row in data]

    @classmethod
    def identity(cls, size):
        data = [[(1.0 if i == j else 0.0) for i in range(size)] for j in range(size)]
        return cls(Shape(size, size), data)

    # 2D rotation matrix (2x2)
    @staticmethod
    def rotation_2d(theta):
        c = math.cos(theta)
        s = math.sin(theta)
        return Matrix(Shape(2, 2), [[c, -s], [s, c]])

    # 2D homogeneous transform 3x3 from rotation (2x2) and translation [tx, ty]
    @staticmethod
    def transform_2d(theta, tx=0.0, ty=0.0):
        r = Matrix.rotation_2d(theta).data
        data = [
            [r[0][0], r[0][1], tx],
            [r[1][0], r[1][1], ty],
            [0.0,     0.0,     1.0],
        ]
        return Matrix(Shape(3, 3), data)

    # Multiply matrix by matrix or matrix by a vector
    def __mul__(self, other):
        if isinstance(other, Matrix):
            a_rows = self.shape.y_size
            a_cols = self.shape.x_size
            b_rows = other.shape.y_size
            b_cols = other.shape.x_size
            if a_cols != b_rows:
                raise ValueError("Shape mismatch for multiplication")
            out = [[0.0] * b_cols for _ in range(a_rows)]
            for i in range(a_rows):
                for j in range(b_cols):
                    s = 0.0
                    for k in range(a_cols):
                        s += self.data[i][k] * other.data[k][j]
                    out[i][j] = s
            return Matrix(Shape(b_cols, a_rows), out)
        elif isinstance(other, (list, tuple)):
            # treat as column vector
            rows = self.shape.y_size
            cols = self.shape.x_size
            if cols != len(other):
                raise ValueError("Vector length mismatch")
            out = [0.0] * rows
            for i in range(rows):
                s = 0.0
                for j in range(cols):
                    s += self.data[i][j] * other[j]
                out[i] = s
            return out
        else:
            raise TypeError("Unsupported multiply")

    def copy(self):
        return Matrix(self.shape, self.data)

    def pretty(self, precision=4):
        str_rows = [[f"{val:.{precision}f}" for val in row] for row in self.data]
        col_widths = [max(len(str_rows[r][c]) for r in range(len(str_rows))) for c in range(len(str_rows[0]))]
        lines = []
        for row in str_rows:
            line = "[ " + "  ".join(f"{val:>{col_widths[i]}}" for i, val in enumerate(row)) + " ]"
            lines.append(line)
        return "\n".join(lines)

    def __repr__(self):
        return self.pretty()

    def __str__(self):
        return self.pretty()


# -------------------------
# Vector helpers
# -------------------------
def vec_sub(a, b):
    return [a[0]-b[0], a[1]-b[1]]

def vec_add(a, b):
    return [a[0]+b[0], a[1]+b[1]]

def vec_len(a):
    return math.hypot(a[0], a[1])

def vec_normalize(a):
    l = vec_len(a)
    if l == 0:
        return [0.0, 0.0]
    return [a[0]/l, a[1]/l]

def clamp(x, low, high):
    return max(low, min(high, x))


# -------------------------
# Forward kinematics
# -------------------------
def forward_kinematics(base_pos, lengths, angles):
    joints = [base_pos[:]]  # start with base
    T = Matrix.transform_2d(0.0, base_pos[0], base_pos[1])
    for l, a in zip(lengths, angles):
        R = Matrix.transform_2d(a, l, 0.0)
        T = T * R
        joints.append([T.data[0][2], T.data[1][2]])
    return joints


# -------------------------
# Stable Jacobian Transpose IK
# -------------------------
def jacobian_transpose_ik(base_pos, lengths, angles, target, step_size=0.4, iterations=20):
    n = len(angles)
    for _ in range(iterations):
        joints = forward_kinematics(base_pos, lengths, angles)
        end = joints[-1]
        error = [target[0] - end[0], target[1] - end[1]]
        if vec_len(error) < 1e-3:
            break

        # build 2xN Jacobian
        J = [[0.0 for _ in range(n)] for _ in range(2)]
        for i in range(n):
            joint = joints[i]
            r = [end[0] - joint[0], end[1] - joint[1]]
            J[0][i] = -r[1]
            J[1][i] =  r[0]

        # delta theta = alpha * J^T * error
        JT = list(zip(*J))  # transpose
        for i in range(n):
            dtheta = step_size * (JT[i][0]*error[0] + JT[i][1]*error[1])
            angles[i] += dtheta
    return angles


# -------------------------
# Pygame demo
# -------------------------
def run_demo():
    pygame.init()
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stable 2D IK (Jacobian Transpose)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    base = [WIDTH//2 - 150, HEIGHT//2 + 50]
    n_links = 4
    lengths = [100, 80, 60, 40]
    angles = [0 for _ in range(n_links)]
    target = [WIDTH//2 + 200, HEIGHT//2 - 50]

    dragging = False
    auto_solve = True
    iterations_per_frame = 10

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx,my = event.pos
                    if vec_len([mx - target[0], my - target[1]]) < 12:
                        dragging = True
                    else:
                        target = [mx,my]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mx,my = event.pos
                target = [mx,my]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    auto_solve = not auto_solve
                elif event.key == pygame.K_UP:
                    iterations_per_frame = clamp(iterations_per_frame + 1, 1, 200)
                elif event.key == pygame.K_DOWN:
                    iterations_per_frame = clamp(iterations_per_frame - 1, 1, 200)
                elif event.key == pygame.K_r:
                    angles = [random.uniform(-0.5, 0.5) for _ in range(n_links)]
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        if auto_solve:
            jacobian_transpose_ik(base, lengths, angles, target, step_size=0.3, iterations=iterations_per_frame)

        # Draw
        screen.fill((30, 30, 35))
        pygame.draw.circle(screen, (220, 80, 80), (int(target[0]), int(target[1])), 8)
        pygame.draw.circle(screen, (220, 150, 150), (int(target[0]), int(target[1])), 4)

        joints = forward_kinematics(base, lengths, angles)
        for i in range(len(joints)-1):
            p0 = joints[i]
            p1 = joints[i+1]
            pygame.draw.line(screen, (200, 200, 200), (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), 6)
            pygame.draw.circle(screen, (120, 180, 240), (int(p0[0]), int(p0[1])), 8)
        ee = joints[-1]
        pygame.draw.circle(screen, (80, 220, 140), (int(ee[0]), int(ee[1])), 8)

        # HUD
        hud_lines = [
            f"Target: {int(target[0])}, {int(target[1])}",
            f"End-effector: {int(ee[0])}, {int(ee[1])}",
            f"Distance: {vec_len(vec_sub(ee, target)):.2f}",
            f"Auto-IK: {'ON' if auto_solve else 'OFF'} (space to toggle)",
            f"Iterations/frame: {iterations_per_frame} (up/down)",
            "Left-drag target or left-click to move",
            "R: randomize angles. ESC to quit."
        ]
        y = 8
        for line in hud_lines:
            surf = font.render(line, True, (220, 220, 220))
            screen.blit(surf, (8, y))
            y += 18

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_demo()
