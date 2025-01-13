class ScrollBufferedScreen:
    def __init__(self, max_lines=12):
        """
        Initialize the ScrollBufferedScreen with a specified maximum number of lines.

        :param max_lines: The maximum number of lines to keep in the buffer (default is 12).
        """
        self.max_lines = max_lines
        self.buffer = []

    def add_line(self, line):
        """
        Add a new line of text to the screen. Oldest lines are discarded once the limit is reached.

        :param line: The new line to add (string).
        """
        self.buffer.append(line)
        # Keep only the most recent `max_lines` lines
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)

    def get_screen_content(self):
        """
        Retrieve the current screen content as a list of lines.

        :return: A list of strings representing the current content of the screen buffer.
        """
        return self.buffer

    def clear_screen(self):
        """
        Clear all lines from the screen buffer.
        """
        self.buffer = []
