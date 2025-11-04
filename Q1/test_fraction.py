import unittest
import sys
from fractionlib import Fraction, MixedFraction

class FractionSuite(unittest.TestCase):
    def test_construct_and_normalize(self):
        self.assertEqual(str(Fraction(10, 20)), "1/2")
        self.assertEqual(Fraction(2, -4), Fraction(-1, 2))
        self.assertEqual(Fraction("  -10 / 20 "), Fraction(-1, 2))
        self.assertEqual(Fraction("7"), Fraction(7, 1))
        self.assertEqual(str(Fraction(-7, 1)), "-7")
        f_orig = Fraction(3, 5)
        f_copy = Fraction(f_orig)
        self.assertEqual(f_orig, f_copy)
        with self.assertRaises(ZeroDivisionError):
            Fraction(1, 0)
        with self.assertRaises(ValueError):
            Fraction("3//4")
        with self.assertRaises(TypeError):
            Fraction("3/4", 2)
        with self.assertRaises(TypeError):
            Fraction(1.5, 2)

    def test_immutability(self):
        f = Fraction(1, 2)

        with self.assertRaises(AttributeError):
            f.numerator = 9

        with self.assertRaises(AttributeError):
            f._numerator = 9

        with self.assertRaises(AttributeError):
            f.value = 10

    def test_arithmetic_ops(self):
        a, b = Fraction(1, 2), Fraction(1, 3)

        self.assertEqual(a + b, Fraction(5, 6))
        self.assertEqual(a - b, Fraction(1, 6))
        self.assertEqual(a * b, Fraction(1, 6))
        self.assertEqual(a / b, Fraction(3, 2))
        self.assertEqual(a + 1, Fraction(3, 2))
        self.assertEqual(1 + a, Fraction(3, 2))
        self.assertEqual(1 - a, Fraction(1, 2))
        self.assertEqual(2 * a, Fraction(1, 1))
        self.assertEqual(3 / a, Fraction(6, 1))

        with self.assertRaises(ZeroDivisionError):
            _ = a / Fraction(0)
        with self.assertRaises(ZeroDivisionError):
            _ = a / 0

    def test_integer_power(self):
        a = Fraction(2, 3)
        self.assertEqual(a ** 0, Fraction(1, 1))
        self.assertEqual(a ** 2, Fraction(4, 9))
        self.assertEqual(a ** -1, Fraction(3, 2))
        with self.assertRaises(ValueError):
            _ = Fraction(0, 1) ** -1
        with self.assertRaises(TypeError):
            _ = a ** 1.5

    def test_equality_and_hash(self):
        a, b = Fraction(2, 4), Fraction(1, 2)

        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        s = {a, Fraction(3, 4)}
        self.assertIn(b, s)
        d = {a: "half"}
        self.assertEqual(d[b], "half")
        self.assertTrue(Fraction(1, 3) < Fraction(1, 2))
        self.assertTrue(Fraction(1, 2) <= Fraction(2, 4))
        self.assertTrue(Fraction(3) > Fraction(2))
        self.assertTrue(Fraction(-1) < 0)

    def test_type_conversion(self):
        f = Fraction(5, 3)
        self.assertAlmostEqual(float(f), 1.6666666666666667)
        self.assertEqual(int(f), 1)
        f_neg = Fraction(-5, 3)
        self.assertEqual(int(f_neg), -1)

    def test_mixed_fraction_display(self):
        self.assertEqual(str(MixedFraction(3, 2)), "1 and 1/2")
        self.assertEqual(str(MixedFraction(10, 3)), "3 and 1/3")
        self.assertEqual(str(MixedFraction(-3, 2)), "-1 and 1/2")
        self.assertEqual(str(MixedFraction(-10, 3)), "-3 and 1/3")
        self.assertEqual(str(MixedFraction(5, 5)), "1")
        self.assertEqual(str(MixedFraction(-5, 5)), "-1")
        self.assertEqual(str(MixedFraction(7, 1)), "7")
        self.assertEqual(str(MixedFraction(2, 4)), "1/2")
        self.assertEqual(str(MixedFraction(-2, 4)), "-1/2")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)