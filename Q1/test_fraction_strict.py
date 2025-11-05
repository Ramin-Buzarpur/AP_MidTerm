import unittest
from fractionlib import Fraction, MixedFraction

class FractionStrictSuite(unittest.TestCase):
    def test_negative_denominator_normalization(self):
        self.assertEqual(Fraction(1, -2), Fraction(-1, 2))
        self.assertEqual(str(Fraction(1, -2)), str(Fraction(-1, 2)))

    def test_zero_numerator(self):
        self.assertEqual(Fraction(0, 5), Fraction(0, 1))
        self.assertEqual(Fraction(0, -7), Fraction(0, 1))

    def test_large_numbers_reduction(self):
        self.assertEqual(Fraction(10_000, 2_500), Fraction(4, 1))

    def test_right_hand_ops_with_int(self):
        self.assertEqual(1 + Fraction(1, 2), Fraction(3, 2))
        self.assertEqual(2 - Fraction(3, 2), Fraction(1, 2))
        self.assertEqual(3 * Fraction(2, 3), Fraction(2, 1))
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / Fraction(0, 1)

    def test_div_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Fraction(1, 2) / Fraction(0, 1)

    def test_power_corner_cases(self):
        self.assertEqual(Fraction(2, 3) ** 0, Fraction(1, 1))
        self.assertEqual(Fraction(2, 3) ** 3, Fraction(8, 27))
        self.assertEqual(Fraction(2, 3) ** -2, Fraction(9, 4))
        with self.assertRaises(ValueError):
            _ = Fraction(0, 1) ** -1

    def test_commutativity_and_basic_identities(self):
        a = Fraction(1, 2); b = Fraction(1, 3)
        self.assertEqual(a + b, b + a)
        self.assertEqual(a * b, b * a)
        self.assertEqual(a - a, Fraction(0, 1))
        self.assertEqual(a / a, Fraction(1, 1))

    def test_hash_consistency_for_equivalent_values(self):
        a = Fraction(2, 4); b = Fraction(1, 2)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        d = {a: "ok"}
        self.assertEqual(d[b], "ok")

    def test_mixed_fraction_display_golden(self):
        cases = [
            (7, 3, "2 and 1/3"),
            (-7, 3, "-2 and 1/3"),
            (2, 3, "2/3"),
            (9, 3, "3"),
            (-2, 3, "-2/3"),
            (-11, 5, "-2 and 1/5"),
        ]
        for n, d, s in cases:
            self.assertEqual(str(MixedFraction(n, d)), s)

if __name__ == "__main__":
    unittest.main(verbosity=2)
