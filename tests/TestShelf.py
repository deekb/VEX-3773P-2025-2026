import unittest
import tempfile
import os
from VEXLib.Util.Shelf import Shelf


class TestShelf(unittest.TestCase):
    def setUp(self):
        # Temporary file for the shelf
        self.temporary_file = tempfile.NamedTemporaryFile(delete=False)
        self.path = self.temporary_file.name
        self.temporary_file.close()
        self.shelf = Shelf(self.path)

    def tearDown(self):
        # Cleanup file after test
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

    def test_set_and_get(self):
        self.shelf.set("int_val", 42)
        self.shelf.set("float_val", 3.14)
        self.shelf.set("str_val", "Hello")
        self.shelf.set("bool_val", True)
        self.shelf.set("none_val", None)
        self.shelf.set("dict_val", {"a": 1, "b": 2})

        self.assertEqual(self.shelf.get("int_val"), 42)
        self.assertAlmostEqual(self.shelf.get("float_val"), 3.14)
        self.assertEqual(self.shelf.get("str_val"), "Hello")
        self.assertTrue(self.shelf.get("bool_val"))
        self.assertIsNone(self.shelf.get("none_val"))
        self.assertEqual(self.shelf.get("dict_val"), {"a": 1, "b": 2})

        # Default value if key missing
        self.assertEqual(self.shelf.get("missing_key", "default"), "default")

    def test_delete(self):
        self.shelf.set("temp", "delete_me")
        self.assertTrue(self.shelf.delete("temp"))
        self.assertFalse(self.shelf.delete("temp"))  # Already deleted
        self.assertIsNone(self.shelf.get("temp"))

    def test_keys_and_items(self):
        self.shelf.set("a", 1)
        self.shelf.set("b", 2)
        keys = self.shelf.keys()
        self.assertIn("a", keys)
        self.assertIn("b", keys)

        items = dict(self.shelf.items())
        self.assertEqual(items["a"], 1)
        self.assertEqual(items["b"], 2)

    def test_persistence(self):
        # Simulate separate program run by reopening shelf
        self.shelf.set("persist", "value")
        self.shelf = Shelf(self.path)  # Reopen
        self.assertEqual(self.shelf.get("persist"), "value")


if __name__ == "__main__":
    unittest.main()
