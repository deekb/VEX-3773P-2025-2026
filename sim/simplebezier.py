import pygame
import numpy as np

# ---------------------------
# Helper functions
# ---------------------------


def line_from_pose(x, y, theta):
    return np.array([x, y]), np.array([np.cos(theta), np.sin(theta)])


def intersect_lines(p0, d0, p2, d2):
    A = np.column_stack((d0, -d2))
    if np.linalg.matrix_rank(A) < 2:
        return (p0 + p2) / 2
    b = p2 - p0
    t_s = np.linalg.solve(A, b)
    t = t_s[0]
    return p0 + t * d0


def quadratic_bezier(t, p0, p1, p2):
    x = (1 - t) * ((1 - t) * p0[0] + t * p1[0]) + t * ((1 - t) * p1[0] + t * p2[0])
    y = (1 - t) * ((1 - t) * p0[1] + t * p1[1]) + t * ((1 - t) * p1[1] + t * p2[1])
    return np.array([x, y])


def bezier_from_poses(start_pose, end_pose):
    p0, d0 = line_from_pose(*start_pose)
    p2, d2 = line_from_pose(*end_pose)
    tangent_intersection = intersect_lines(p0, d0, p2, -d2)
    midpoint = (p0 + p2) / 2
    p1 = midpoint + tangent_intersection - midpoint
    return p0, p1, p2

def bezier_derivatives(p0, p1, p2, t):
    # First derivative
    dB = 2 * (1 - t) * (p1 - p0) + 2 * t * (p2 - p1)
    # Second derivative
    ddB = 2 * (p2 - 2*p1 + p0)
    return dB, ddB

def curvature(p0, p1, p2, t):
    dB, ddB = bezier_derivatives(p0, p1, p2, t)
    dx, dy = dB
    ddx, ddy = ddB
    kappa = abs(dx*ddy - dy*ddx) / (dx**2 + dy**2)**1.5
    return kappa

# ---------------------------
# Pygame setup
# ---------------------------

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# Initial poses
start_pose = [100, 500, np.radians(45)]
end_pose = [700, 100, np.radians(135)]


dragging_point = None
dragging_heading = None
heading_length = 50  # length of the heading handle


def is_mouse_near_point(mouse, point, radius=10):
    return np.linalg.norm(np.array(mouse) - np.array(point)) < radius


running = True
while running:
    screen.fill((30, 30, 30))

    mouse = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_mouse_near_point(mouse, start_pose[:2]):
                dragging_point = start_pose
            elif is_mouse_near_point(mouse, end_pose[:2]):
                dragging_point = end_pose
            else:
                # Check heading handles
                start_head = start_pose[:2] + heading_length * np.array(
                    [np.cos(start_pose[2]), np.sin(start_pose[2])]
                )
                end_head = end_pose[:2] + heading_length * np.array(
                    [np.cos(end_pose[2]), np.sin(end_pose[2])]
                )
                if is_mouse_near_point(mouse, start_head):
                    dragging_heading = start_pose
                elif is_mouse_near_point(mouse, end_head):
                    dragging_heading = end_pose
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_point = None
            dragging_heading = None

    # Dragging
    if dragging_point:
        dragging_point[0], dragging_point[1] = mouse
    if dragging_heading:
        dx, dy = mouse[0] - dragging_heading[0], mouse[1] - dragging_heading[1]
        dragging_heading[2] = np.arctan2(dy, dx)

    # Compute Bézier
    p0, p1, p2 = bezier_from_poses(start_pose, end_pose)
    import matplotlib.pyplot as plt

    # Compute curvature along the Bézier
    t_values = np.linspace(0, 1, 101)
    curvatures = [curvature(p0, p1, p2, t) for t in t_values]

    # Plot curvature
    plt.figure(figsize=(8, 4))
    plt.plot(t_values, curvatures, color="orange", linewidth=2)
    plt.title("Curvature along Bézier path")
    plt.xlabel("t (normalized path parameter)")
    plt.ylabel("Curvature κ")
    plt.grid(True)
    plt.show()

    bezier_points = [quadratic_bezier(t / 100, p0, p1, p2) for t in range(101)]

    # Draw Bézier curve
    for i in range(len(bezier_points) - 1):
        pygame.draw.line(
            screen, (0, 200, 255), bezier_points[i], bezier_points[i + 1], 3
        )

    # Draw control points
    for pt in [p0, p1, p2]:
        pygame.draw.circle(screen, (255, 100, 100), pt.astype(int), 8)

    # Draw headings
    for pos, pose, color in [
        (p0, start_pose, (0, 255, 0)),
        (p2, end_pose, (255, 255, 0)),
    ]:
        x, y = pos
        dx = np.cos(pose[2]) * heading_length
        dy = np.sin(pose[2]) * heading_length
        pygame.draw.line(screen, color, (x, y), (x + dx, y + dy), 3)
        pygame.draw.circle(
            screen, color, (int(x + dx), int(y + dy)), 6
        )  # heading handle

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
