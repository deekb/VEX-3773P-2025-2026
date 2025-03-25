class CircularBuffer:
    def __init__(self, length):
        self.length = length
        self.buffer = []
        self.index = 0

    def add(self, data):
        if len(self.buffer) < self.length:
            self.buffer.append(data)
        else:
            self.buffer[self.index] = data
        self.index = (self.index + 1) % self.length

    def get(self):
        return self.buffer

    def clear(self):
        self.buffer = []
        self.index = 0

    def initialize(self, value):
        self.buffer = [value] * self.length
        self.index = 0
