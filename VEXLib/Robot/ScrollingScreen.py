from VEXLib.Util import enumerate
from vex import FontType


class ScrollBufferedScreen:
    def __init__(self, screen, max_lines=12):
        """
        Initialize the ScrollBufferedScreen with a specified maximum number of lines.

        :param max_lines: The maximum number of lines to keep in the buffer (default is 12).
        """
        self.screen = screen
        self.max_lines = max_lines
        self.buffer = []

    def add_line_to_buffer(self, line):
        """
        Add a new line of text to the screen. Oldest lines are discarded once the limit is reached.

        :param line: The new line to add (string).
        """
        self.buffer.append(line)
        # Keep only the most recent `max_lines` lines
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)

    def get_buffer_content(self):
        """
        Retrieve the current screen content as a list of lines.

        :return: A list of strings representing the current content of the screen buffer.
        """
        return self.buffer

    def clear_buffer(self):
        """
        Clear all lines from the screen buffer.
        """
        self.buffer = []

    def print(self, *parts):
        self.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.add_line_to_buffer(message)
        self.render_screen_contents()

    def render_screen_contents(self):
        for row, line in enumerate(self.screen.get_screen_content()):
            self.screen.set_cursor(row, 1)
            self.screen.clear_row(row)
            self.screen.print(line)
