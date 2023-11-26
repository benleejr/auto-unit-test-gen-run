from uploads.math_testing_reverse_sub import add, sub, multi, div
import unittest

import unittest

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(5, 10)
        self.assertEqual(result, 15)

    def test_add_negative_numbers(self):
        result = add(-5, -10)
        self.assertEqual(result, -15)

    def test_add_positive_and_negative_numbers(self):
        result = add(5, -10)
        self.assertEqual(result, -5)

    def test_add_zero(self):
        result = add(5, 0)
        self.assertEqual(result, 5)


class TestSub(unittest.TestCase):
    def test_sub_positive_numbers(self):
        result = sub(10, 5)
        self.assertEqual(result, 5)

    def test_sub_negative_numbers(self):
        result = sub(-5, -10)
        self.assertEqual(result, 5)

    def test_sub_positive_and_negative_numbers(self):
        result = sub(-5, 10)
        self.assertEqual(result, 15)

    def test_sub_zero(self):
        result = sub(5, 0)
        self.assertEqual(result, -5)


class TestMulti(unittest.TestCase):
    def test_multi_positive_numbers(self):
        result = multi(5, 10)
        self.assertEqual(result, 50)

    def test_multi_negative_numbers(self):
        result = multi(-5, -10)
        self.assertEqual(result, 50)

    def test_multi_positive_and_negative_numbers(self):
        result = multi(-5, 10)
        self.assertEqual(result, -50)

    def test_multi_zero(self):
        result = multi(5, 0)
        self.assertEqual(result, 0)


class TestDiv(unittest.TestCase):
    def test_div_positive_numbers(self):
        result = div(10, 5)
        self.assertEqual(result, 2)

    def test_div_negative_numbers(self):
        result = div(-10, -5)
        self.assertEqual(result, 2)

    def test_div_positive_and_negative_numbers(self):
        result = div(-10, 5)
        self.assertEqual(result, -2)

    def test_div_zero(self):
        result = div(5, 0)
        self.assertRaises(ZeroDivisionError)


if __name__ == '__main__':
    unittest.main()