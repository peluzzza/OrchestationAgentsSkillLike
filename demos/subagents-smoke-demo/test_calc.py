from __future__ import annotations

from pathlib import Path
import sys
import unittest


_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import calc


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 4), 6)

    def test_multiply(self):
        self.assertEqual(calc.multiply(6, 7), 42)

    def test_divide(self):
        self.assertEqual(calc.divide(8, 2), 4)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            calc.divide(1, 0)


if __name__ == "__main__":
    unittest.main()
