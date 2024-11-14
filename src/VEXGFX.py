from vex import Color

class Button:
    def __init__(self, screen, x: int, y: int, width: int, height: int, text="", image=None, text_color=Color.BLACK, fill_color=Color.BLUE, is_visible=True):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.text_color = text_color
        self.fill_color = fill_color
        self.pressed_callback = None
        self.released_callback = None
        self.is_pressed = False
        self.is_visible = is_visible
        self.needs_redraw = True  # Track if the button needs to be redrawn

    def draw(self):
        if self.needs_redraw:
            if self.is_visible:
                # Draw the button rectangle
                self.screen.set_pen_color(self.fill_color)
                self.screen.set_fill_color(self.fill_color)
                self.screen.draw_rectangle(self.x, self.y, self.width, self.height)

                # Draw the button text or image
                if self.image:
                    self.screen.draw_image_from_file(self.image, self.x + self.width // 2 - 10, self.y + self.height // 2 - 10)
                if self.text:
                    self.screen.set_pen_color(self.text_color)
                    text_width = self.screen.get_string_width(self.text)
                    text_height = self.screen.get_string_height(self.text)
                    text_x = self.x + (self.width - text_width) // 2
                    text_y = self.y + (self.height - text_height) // 2
                    self.screen.print_at(self.text, x=text_x, y=text_y)
            else:
                self.screen.set_fill_color(Color.BLACK)
                self.screen.set_pen_color(Color.BLACK)
                self.screen.draw_rectangle(self.x, self.y, self.width, self.height)

            # Reset needs_redraw after drawing
            self.needs_redraw = False

    def hide(self):
        self.is_visible = False
        self.needs_redraw = True  # Mark for redraw

    def show(self):
        self.is_visible = True
        self.needs_redraw = True  # Mark for redraw

    def set_pressed_callback(self, callback):
        self.pressed_callback = callback

    def set_released_callback(self, callback):
        self.released_callback = callback

    def check_press(self, x, y, is_currently_pressed):
        # Check if the button is pressed
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            if is_currently_pressed and not self.is_pressed:
                # Button was just pressed
                self.is_pressed = True
                self.needs_redraw = True  # Mark for redraw
                if self.pressed_callback:
                    self.pressed_callback()
            elif not is_currently_pressed and self.is_pressed:
                # Button was just released
                self.is_pressed = False
                self.needs_redraw = True  # Mark for redraw
                if self.released_callback:
                    self.released_callback()
        elif not is_currently_pressed and self.is_pressed:
            # If touch is outside the button but the button was previously pressed
            self.is_pressed = False
            self.needs_redraw = True  # Mark for redraw
            if self.released_callback:
                self.released_callback()


class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    def create_button(self, x, y, width, height, text="", image=None, text_color=Color.WHITE, fill_color=Color.BLUE, is_visible=True):
        button = Button(self.screen, x, y, width, height, text, image, text_color, fill_color, is_visible)
        self.buttons.append(button)
        button.draw()  # Initial draw
        return button

    def handle_touch(self):
        is_currently_pressed = self.screen.pressing()
        touch_x = self.screen.x_position()
        touch_y = self.screen.y_position()

        for button in self.buttons:
            button.check_press(touch_x, touch_y, is_currently_pressed)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()  # Will only draw if needs_redraw is True


from VEXLib.Robot.NewTickBasedRobot import TickBasedRobot

class Robot(TickBasedRobot):
    def __init__(self, brain, autonomous):
        super().__init__(brain)
        # Example usage
        # self._target_tick_duration_ms = 50
        # self._warning_tick_duration_ms = 75
        self.screen = self.brain.screen
        self.graphics = Graphics(self.screen)
        self.red_button = None
        self.blue_button = None
        self.restart_button = None
        self.back_button = None

    def on_setup(self):
        # self.screen.draw_image_from_file("deploy/background.png", 0, 0)
        self.restart_button = self.graphics.create_button(0, 0, 100, 40, text="Restart", fill_color=Color.PURPLE)
        self.back_button = self.graphics.create_button(380, 0, 100, 40, text="Back", fill_color=Color.ORANGE)
        self.restart_button.set_released_callback(self.trigger_restart)
        self.select_team()

    def select_team(self):
        self.red_button = self.graphics.create_button(0, 40, 240, 200, text="Red", fill_color=Color.RED)
        self.blue_button = self.graphics.create_button(240, 40, 240, 200, text="Blue", fill_color=Color.BLUE)
        self.red_button.set_released_callback(lambda: print("Red Release"))
        self.back_button.set_released_callback(lambda: (self.red_button.hide(),
                                                        self.blue_button.hide(),
                                                        self.on_setup())
                                               )



    def periodic(self):
        # pass
        # self.brain.screen.clear_screen()
        self.graphics.draw_buttons()  # Only redraw buttons that need it
        self.graphics.handle_touch()
