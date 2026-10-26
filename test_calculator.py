import unittest

from calculator import calculate, fmt


class TestCalculate(unittest.TestCase):
    def test_operations(self):
        self.assertEqual(calculate(2, 3, "+"), 5)
        self.assertEqual(calculate(2, 3, "-"), -1)
        self.assertEqual(calculate(2, 3, "*"), 6)
        self.assertEqual(calculate(7, 2, "/"), 3.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0, "/")

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            calculate(1, 2, "^")

    def test_format(self):
        self.assertEqual(fmt(7.0), "7")
        self.assertEqual(fmt(0.1 + 0.2), "0.3")


if __name__ == "__main__":
    unittest.main()
