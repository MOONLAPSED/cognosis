import unittest
from uutils_ import Uutils_
from main import main

class TestUutils(unittest.TestCase):

    def test_main(self):
        obj = Uutils_()
        expected_result = ...
        result = ...
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()