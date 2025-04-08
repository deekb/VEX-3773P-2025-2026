class Buffer:
    def __init__(self, length):
        self.length = length
        self.buffer = []

    def add(self, data):
        if len(self.buffer) >= self.length:
            self.buffer.pop(0)
        self.buffer.append(data)

    def get(self):
        return self.buffer

    def clear(self):
        self.buffer = []

    def initialize(self, value):
        self.buffer = [value] * self.length
