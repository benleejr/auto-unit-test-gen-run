from uploads.math_testing_divide_by_zero import add, sub, multi, div
import unittest

import unittest

class TestMathFunctions(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-2, 3), 1)
        self.assertEqual(add(0, 0), 0)
    
    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)
        self.assertEqual(sub(-2, -2), 0)
        self.assertEqual(sub(0, 0), 0)
    
    def test_multi(self):
        self.assertEqual(multi(2, 3), 6)
        self.assertEqual(multi(-2, 3), -6)
        self.assertEqual(multi(0, 5), 0)
    
    def test_div(self):
        with self.assertRaises(ZeroDivisionError):
            div(2, 0)
        self.assertEqual(div(6, 3), 2)
        self.assertEqual(div(-6, 3), -2)
        self.assertEqual(div(0, 5), 0)

if __name__ == '__main__':
    unittest.main()