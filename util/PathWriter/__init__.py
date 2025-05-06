import math

import pygame

from util.PathWriter.Splines import CatmullRomSpline

# Settings for the control points and spline behavior
CONTROL_POINT_RADIUS = 3  # Radius for drawing control points
POINT_SELECTION_RADIUS = 20  # Radius for selecting control points
FIELD_SIZE_CM = (365.76, 365.76)
SCREEN_SCALING_FACTOR = 2.8


def rescale_point(point):
    return point[0] * SCREEN_SCALING_FACTOR, point[1] * SCREEN_SCALING_FACTOR


# Initialize pygame
pygame.init()

# Set up display
clock = pygame.time.Clock()
pygame.display.set_caption("Connected Splines")
screen = pygame.display.set_mode(rescale_point(FIELD_SIZE_CM), pygame.RESIZABLE)


# Function to find the nearest control point
def find_nearest_control_point(control_points, position):
    """Finds the index of the control point nearest to the given position."""
    for index, point in enumerate(control_points):
        distance = math.sqrt(
            (position[0] - point[0]) ** 2 + (position[1] - point[1]) ** 2
        )
        if distance <= POINT_SELECTION_RADIUS:
            return index
    return None


# Button class for UI
class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, self.rect.center)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Main loop
def main():
    global screen
    # Data structures to store control points, curve points, and the currently dragged point
    control_points = []  # List of control points defined by the user
    spline_points = []  # Points along the generated spline
    dragging_point = None  # Index of the currently dragged control point
    action_points = []  # List to store actions
    action_buttons = []  # List of buttons for actions

    spline_type = CatmullRomSpline()  # Swap between CatmullRomSpline and NURBSSpline here
    running = True

    # Create action buttons
    # add_point_button = Button(1050, 100, 120, 50, (0, 255, 0), "Add Action", action="add_point")
    # action_buttons.append(add_point_button)

    while running:
        # Fill the screen with a background color
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if event.button == 1:  # Left click
                    # On mouse click, check if a control point is selected or if a new one is added
                    selected_point_index = find_nearest_control_point(control_points, mouse_position)
                    if selected_point_index is not None:
                        # Start dragging the selected control point
                        dragging_point = selected_point_index
                    else:
                        # Add a new control point and regenerate the spline
                        control_points.append(list(mouse_position))
                        if len(control_points) >= 2:
                            spline_points = spline_type.generate(control_points)
                elif event.button == 2:
                    print("finding closest spline point")
                    find_nearest_control_point(spline_points, mouse_position)

                    # Check if any action button is clicked
                    for button in action_buttons:
                        if button.is_clicked(mouse_position):
                            if button.action == "add_point":
                                actions.append({"action": "change_color", "percent": 50})
            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop dragging the control point
                dragging_point = None

            elif event.type == pygame.MOUSEMOTION and dragging_point is not None:
                # Update the dragged control point position
                control_points[dragging_point] = list(pygame.mouse.get_pos())
                if len(control_points) >= 2:
                    spline_points = spline_type.generate(control_points)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    print("Exporting spline data")
                    with open("spline_data.txt", "w") as f:
                        f.write(str(spline_points))

        # Draw the control polygon (lines connecting control points)
        if len(control_points) > 1:
            pygame.draw.lines(screen, (100, 100, 255), False, control_points, 1)

        # Draw each control point as a circle
        for point in control_points:
            pygame.draw.circle(screen, (255, 100, 100), point, CONTROL_POINT_RADIUS)

        # Draw the generated spline curve
        if len(spline_points) > 1:
            for point in spline_points:
                pygame.draw.circle(screen, (255, 0, 255), point, CONTROL_POINT_RADIUS)
            pygame.draw.lines(screen, (0, 255, 0), False, spline_points, 2)

        # Draw action buttons
        for button in action_buttons:
            button.draw(screen)

        # Apply actions (for now, just changing color at a percentage)
        # for action in actions:
        #     if action['action'] == 'change_color':
        #         percent = action['percent']
        #         index = int(percent / 100 * len(spline_points))
        #         if 0 <= index < len(spline_points):
        #             pygame.draw.circle(screen, (0, 0, 255), spline_points[index], CONTROL_POINT_RADIUS)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    # Quit pygame when the loop ends
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cleanly...")
        pygame.quit()
