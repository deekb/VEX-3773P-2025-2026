import unittest
import hashlib
from VEXLib.Util.MD5sum import md5sum


class TestMD5Functions(unittest.TestCase):

    def test_md5sum_match_builtin(self):
        # Test case for the md5sum function
        test_data = "hello world".encode("utf-8")  # You can modify this as needed

        # Compute MD5 using the provided md5sum function
        custom_md5 = md5sum(test_data)

        # Compute MD5 using Python's built-in hashlib
        builtin_md5 = hashlib.md5(test_data).hexdigest()

        # Assert that both MD5 hashes match
        self.assertEqual(custom_md5, builtin_md5)


if __name__ == '__main__':
    unittest.main()
