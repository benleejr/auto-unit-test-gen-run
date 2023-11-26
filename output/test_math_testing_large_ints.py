from uploads.math_testing_large_ints import add, sub, multi, div
import unittest

import unittest
import random


class TestAdd(unittest.TestCase):
    def test_add(self):
        result = add()
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


class TestSub(unittest.TestCase):
    def test_sub(self):
        result = sub(5, 3)
        self.assertEqual(result, 2)

        result = sub(10, 2)
        self.assertEqual(result, 8)

        result = sub(-5, -3)
        self.assertEqual(result, -2)


class TestMulti(unittest.TestCase):
    def test_multi(self):
        result = multi(5, 3)
        self.assertEqual(result, 15)

        result = multi(10, 0)
        self.assertEqual(result, 0)

        result = multi(-5, -3)
        self.assertEqual(result, 15)


class TestDiv(unittest.TestCase):
    def test_div(self):
        result = div(10, 2)
        self.assertEqual(result, 5)

        result = div(12, 3)
        self.assertAlmostEqual(result, 4)

        result = div(10, 3)
        self.assertAlmostEqual(result, 3.3333333, places=6)


if __name__ == '__main__':
    unittest.main()