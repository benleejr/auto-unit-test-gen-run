from uploads.math_testing import add, sub, multi, div
import unittest

import unittest

class TestAdd(unittest.TestCase):
    def test_add_positive(self):
        result = add(3, 4)
        self.assertEqual(result, 7)
        
    def test_add_negative(self):
        result = add(-3, -4)
        self.assertEqual(result, -7)
        
    def test_add_zero(self):
        result = add(0, 4)
        self.assertEqual(result, 4)
        
class TestSub(unittest.TestCase):
    def test_sub_positive(self):
        result = sub(10, 4)
        self.assertEqual(result, 6)
        
    def test_sub_negative(self):
        result = sub(-10, -4)
        self.assertEqual(result, -6)
        
    def test_sub_zero(self):
        result = sub(10, 0)
        self.assertEqual(result, 10)

class TestMulti(unittest.TestCase):
    def test_multi_positive(self):
        result = multi(3, 4)
        self.assertEqual(result, 12)
        
    def test_multi_negative(self):
        result = multi(-3, -4)
        self.assertEqual(result, 12)
        
    def test_multi_zero(self):
        result = multi(0, 4)
        self.assertEqual(result, 0)
        
class TestDiv(unittest.TestCase):
    def test_div_positive(self):
        result = div(10, 2)
        self.assertEqual(result, 5)
        
    def test_div_negative(self):
        result = div(-10, -2)
        self.assertEqual(result, 5)
        
    def test_div_zero(self):
        result = div(0, 4)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()