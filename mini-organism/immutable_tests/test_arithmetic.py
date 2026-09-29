"""Immutable acceptance tests for workspace/arithmetic.py.

Run from mini-organism/:

    python3 -m unittest -v immutable_tests.test_arithmetic

Each function is looked up inside its own test, so a missing multiply()
fails only the multiply tests and add() is still checked independently.
"""

import unittest

from workspace import arithmetic


class TestAdd(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(arithmetic.add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(arithmetic.add(-1, 1), 0)


class TestMultiply(unittest.TestCase):
    def test_multiply_positive(self):
        self.assertEqual(arithmetic.multiply(2, 3), 6)

    def test_multiply_negative(self):
        self.assertEqual(arithmetic.multiply(-2, 4), -8)

    def test_multiply_zero(self):
        self.assertEqual(arithmetic.multiply(0, 99), 0)


if __name__ == "__main__":
    unittest.main()
