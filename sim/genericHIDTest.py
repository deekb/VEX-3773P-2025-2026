import pygame
import sys
from collections import deque

# ----------------------------
# Configuration
# ----------------------------
SCALE = 3  # UI scale factor
WIDTH, HEIGHT = int(500 * SCALE), int(600 * SCALE)
FPS = 120
MAX_TRAIL_LENGTH = 30  # number of past positions to store

AXIS_NAMES = ["LX", "LY", "RX", "RY"]
BUTTON_NAMES = [
    "B", "A", "Y", "X",
    "L1", "R1", "L2", "R2",
    "Back", "-", "-", "-",
    "UP", "DOWN", "LEFT", "RIGHT"
]

STICK_RADIUS = int(50 * SCALE)
DOT_RADIUS = int(8 * SCALE)
BUTTON_SIZE = int(30 * SCALE)
BUTTON_SPACING = int(40 * SCALE)

# ----------------------------
# Initialize pygame
# ----------------------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick found!")
    sys.exit(1)

joy = pygame.joystick.Joystick(0)
joy.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VEX Controller Visualizer")
font = pygame.font.SysFont("consolas", int(22 * SCALE))
clock = pygame.time.Clock()

# ----------------------------
# Trails storage
# ----------------------------
left_trail = deque(maxlen=MAX_TRAIL_LENGTH)
right_trail = deque(maxlen=MAX_TRAIL_LENGTH)

# ----------------------------
# Drawing functions
# ----------------------------
def draw_text(surface, text, x, y, color=(255, 255, 255)):
    surface.blit(font.render(text, True, color), (x, y))

def draw_stick(surface, x, y, axis_x, axis_y, label, trail=None):
    """Draw analog stick with trail."""
    pygame.draw.circle(surface, (100, 100, 100), (x, y), STICK_RADIUS, 2)

    # Add current position to trail
    pos = (x + int(axis_x * STICK_RADIUS), y + int(axis_y * STICK_RADIUS))
    if trail is not None:
        trail.appendleft(pos)  # newest at front

    # Draw trail dots (smaller and more transparent for older points)
    if trail is not None:
        for i, (tx, ty) in enumerate(trail):
            alpha = max(50, 255 - (i * 255 // MAX_TRAIL_LENGTH))
            radius = max(2, DOT_RADIUS - i * DOT_RADIUS // MAX_TRAIL_LENGTH)
            trail_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (0, 200, 0, alpha), (radius, radius), radius)
            surface.blit(trail_surf, (tx - radius, ty - radius))

    # Draw current dot
    pygame.draw.circle(surface, (0, 200, 0), pos, DOT_RADIUS)
    draw_text(surface, label, x - 20 * SCALE, y + STICK_RADIUS + 10 * SCALE)

def draw_buttons(surface, states):
    x, y = 20 * SCALE, 300 * SCALE
    for i, name in enumerate(BUTTON_NAMES):
        if name == "-":
            continue
        color = (0, 200, 0) if states[i] else (100, 50, 50)
        pygame.draw.rect(surface, color, (x, y, BUTTON_SIZE, BUTTON_SIZE))
        draw_text(surface, name, x + 40 * SCALE, y + 5 * SCALE)
        y += BUTTON_SPACING
        if y > HEIGHT - 50 * SCALE:
            y = 300 * SCALE
            x += 200 * SCALE

# ----------------------------
# Main loop
# ----------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((0, 0, 0))

    # --- Read axes (native pygame [-1,1]) ---
    axes = [joy.get_axis(i) for i in range(4)]
    draw_stick(win, int(150 * SCALE), int(120 * SCALE), axes[0], axes[1], "Left Stick", left_trail)
    draw_stick(win, int(350 * SCALE), int(120 * SCALE), axes[2], axes[3], "Right Stick", right_trail)

    # --- Read buttons ---
    buttons = [joy.get_button(i) for i in range(16)]
    draw_buttons(win, buttons)

    # --- Read D-pad (hat) ---
    hat = joy.get_hat(0)
    draw_text(win, f"Hat: {hat}", int(20 * SCALE), int(260 * SCALE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
