from VEXLib.Util import enumerate
from vex import FontType


class ScrollingScreen:
    def __init__(self, screen, buffer):
        """
        Initialize the ScrollingScreen with a specified buffer.

        Args:
            screen: The screen object to display the text.
            buffer: An buffer to store the lines of text.
        """
        self.screen = screen
        self.buffer = buffer

    def add_line_to_buffer(self, line):
        """
        Add a new line of text to the buffer. Oldest lines are discarded once the buffer limit is reached.

        Args:
            line: The new line to add (string).
        """
        self.buffer.add(line)

    def get_buffer_content(self):
        """
        Retrieve the current buffer content as a list of lines.

        Returns:
             A list of strings representing the current content of the buffer.
        """
        return self.buffer.get()

    def clear_buffer(self):
        """
        Clear all lines from the buffer.
        """
        self.buffer.clear()

    def print(self, *parts):
        """
        Print a message composed of the given parts to the screen and add it to the buffer.

        Args:
            parts: Parts of the message to print (strings).
        """
        self.screen.set_font(FontType.MONO15)
        message = " ".join(map(str, parts))
        self.add_line_to_buffer(message)
        self.render_screen_contents()

    def render_screen_contents(self):
        """
        Render the current contents of the buffer to the screen.
        """
        for row, line in enumerate(self.buffer.get()):
            self.screen.set_cursor(row, 1)
            self.screen.clear_row(row)
            self.screen.print(line)
