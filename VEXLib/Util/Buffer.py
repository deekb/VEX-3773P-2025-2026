class Buffer:
    """
    A class to represent a circular buffer with a fixed length.

    Attributes:
        length (int): The maximum number of elements the buffer can hold.
        buffer (list): The list storing the elements of the buffer.

    Methods:
        add(data):
            Adds an element to the buffer. If the buffer is full, the oldest element is removed.
        get():
            Returns the current contents of the buffer.
        clear():
            Clears all elements from the buffer.
        initialize(value):
            Fills the buffer with a specified value, up to its maximum length.
    """

    def __init__(self, length):
        """
        Initializes the Buffer instance with a specified length.

        Args:
            length (int): The maximum number of elements the buffer can hold.
        """
        self.length = length
        self.buffer = []

    def add(self, data):
        """
        Adds an element to the buffer. If the buffer is full, the oldest element is removed.

        Args:
            data: The element to add to the buffer.
        """
        if len(self.buffer) >= self.length:
            self.buffer.pop(0)
        self.buffer.append(data)

    def get(self):
        """
        Retrieves the current contents of the buffer.

        Returns:
            list: The elements currently in the buffer.
        """
        return self.buffer

    def clear(self):
        """
        Clears all elements from the buffer.
        """
        self.buffer = []

    def initialize(self, value):
        """
        Fills the buffer with a specified value, up to its maximum length.

        Args:
            value: The value to fill the buffer with.
        """
        self.buffer = [value] * self.length