import unittest

from VEXLib.Util.CRC import crc_bytes, crc_string, crc_lookup_table


class TestCRC(unittest.TestCase):

    def test_initialization(self):
        self.assertEqual(len(crc_lookup_table), 256)

    def test_crc_bytes(self):
        print(crc_bytes(b"Hello World"))

    def test_is_deterministic(self):
        self.assertEqual(crc_string("Hello World"), crc_string("Hello World"))

    def test_for_unique_outputs(self):
        self.assertNotEqual(crc_string("Hello World"), crc_string("Hello World!"))

    def test_crc_string(self):
        crc_string("Hello World")

    def test_crc_string_empty(self):
        crc_string("")

    def test_crc_bytes_empty(self):
        crc_bytes(b"")

    def test_list_of_ints_input(self):
        self.assertEqual(crc_bytes([72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]), crc_string("Hello World"))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            crc_bytes(None)
        with self.assertRaises(TypeError):
            print(crc_bytes(-100))
        with self.assertRaises(Exception):
            print(crc_bytes([-100]))
        with self.assertRaises(TypeError):
            crc_bytes(["a", "b", "c"])


if __name__ == '__main__':
    unittest.main()
