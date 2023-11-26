from uploads.math_testing_a_exponent import add, sub, multi, div
import unittest

import unittest

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        result = add(-2, -3)
        self.assertEqual(result, -5)

    def test_add_positive_negative_numbers(self):
        result = add(2, -3)
        self.assertEqual(result, -1)

class TestSub(unittest.TestCase):
    def test_sub_positive_numbers(self):
        result = sub(5, 2)
        self.assertEqual(result, 3)

    def test_sub_negative_numbers(self):
        result = sub(-5, -2)
        self.assertEqual(result, -3)

    def test_sub_positive_negative_numbers(self):
        result = sub(2, -3)
        self.assertEqual(result, 5)

class TestMulti(unittest.TestCase):
    def test_multi_positive_numbers(self):
        result = multi(2, 3)
        self.assertEqual(result, 8)

    def test_multi_negative_numbers(self):
        result = multi(-2, -3)
        self.assertEqual(result, -8)

    def test_multi_positive_negative_numbers(self):
        result = multi(2, -3)
        self.assertEqual(result, 0.125)

class TestDiv(unittest.TestCase):
    def test_div_positive_numbers(self):
        result = div(6, 3)
        self.assertEqual(result, 2)

    def test_div_negative_numbers(self):
        result = div(-6, -3)
        self.assertEqual(result, 2)

    def test_div_positive_negative_numbers(self):
        result = div(6, -3)
        self.assertEqual(result, -2)

if __name__ == '__main__':
    unittest.main()