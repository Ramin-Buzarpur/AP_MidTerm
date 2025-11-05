
import unittest, random
from fractions import Fraction as PF
from fractionlib import Fraction

RANGE = 50
def to_our(pf: PF) -> Fraction:
    return Fraction(pf.numerator, pf.denominator)

class FractionOracleSuite(unittest.TestCase):
    def test_random_ops_against_python_fraction(self):
        random.seed(1337)
        for _ in range(300):
            a = random.randint(-RANGE, RANGE)
            b = random.randint(-RANGE, RANGE) or 1  # denom != 0
            c = random.randint(-RANGE, RANGE)
            d = random.randint(-RANGE, RANGE) or 1

            x = Fraction(a, b)
            y = Fraction(c, d)
            X = PF(a, b)
            Y = PF(c, d)
            self.assertEqual(x + y, to_our(X + Y))
            self.assertEqual(x - y, to_our(X - Y))
            self.assertEqual(x * y, to_our(X * Y))
            if Y != PF(0, 1):
                self.assertEqual(x / y, to_our(X / Y))
            else:
                with self.assertRaises(ZeroDivisionError):
                    _ = x / y

            k = random.randint(-7, 7)
            self.assertEqual(x + k, to_our(X + k))
            self.assertEqual(k + x, to_our(k + X))
            self.assertEqual(x - k, to_our(X - k))
            self.assertEqual(k - x, to_our(k - X))
            self.assertEqual(x * k, to_our(X * k))
            self.assertEqual(k * x, to_our(k * X))
            if k != 0:
                self.assertEqual(x / k, to_our(X / k))
                if x == Fraction(0, 1):
                    with self.assertRaises(ZeroDivisionError): _ = k / x
                else:
                    self.assertEqual(k / x, to_our(k / X))
            else:
                with self.assertRaises(ZeroDivisionError): _ = x / k
                if x == Fraction(0, 1):
                    with self.assertRaises(ZeroDivisionError): _ = k / x
                else:
                    self.assertEqual(k / x, to_our(PF(k, 1) / X))
            e = random.choice([-3, -2, -1, 0, 1, 2, 3])
            if e < 0 and x == Fraction(0, 1):
                with self.assertRaises(ValueError):
                    _ = x ** e
            else:
                self.assertEqual(x ** e, to_our(X ** e))

    def test_ordering_consistency(self):
        random.seed(4242)
        for _ in range(200):
            a, b = random.randint(-RANGE, RANGE), random.randint(-RANGE, RANGE) or 1
            c, d = random.randint(-RANGE, RANGE), random.randint(-RANGE, RANGE) or 1
            x, y = Fraction(a, b), Fraction(c, d)
            X, Y = PF(a, b), PF(c, d)
            self.assertEqual(x == y, X == Y)
            self.assertEqual(x < y, X < Y)
            self.assertEqual(x <= y, X <= Y)
            self.assertEqual(x > y, X > Y)
            self.assertEqual(x >= y, X >= Y)

if __name__ == "__main__":
    unittest.main(verbosity=2)
