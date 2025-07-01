import unittest

from VEXLib.Util.Buffer import Buffer


class TestBuffer(unittest.TestCase):

    def test_initialization(self):
        buffer = Buffer(3)
        self.assertEqual(buffer.length, 3)
        self.assertEqual(buffer.buffer, [])

    def test_add(self):
        buffer = Buffer(3)
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)
        self.assertEqual(buffer.get(), [1, 2, 3])
        buffer.add(4)
        self.assertEqual(buffer.get(), [2, 3, 4])
        buffer.add(5)
        self.assertEqual(buffer.get(), [3, 4, 5])
        buffer.add(6)
        self.assertEqual(buffer.get(), [4, 5, 6])

    def test_get(self):
        buffer = Buffer(3)
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)
        self.assertEqual(buffer.get(), [1, 2, 3])

    def test_clear(self):
        buffer = Buffer(3)
        buffer.add(1)
        buffer.add(2)
        buffer.add(3)
        buffer.clear()
        self.assertEqual(buffer.get(), [])

    def test_initialize(self):
        buffer = Buffer(3)
        buffer.initialize(5)
        self.assertEqual(buffer.get(), [5, 5, 5])


if __name__ == '__main__':
    unittest.main()
