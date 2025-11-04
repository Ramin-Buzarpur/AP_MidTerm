from fractionlib import Fraction, MixedFraction

assert Fraction(2, -4) == Fraction(-1, 2)
assert Fraction("-15/20") == Fraction(-3, 4)
assert Fraction("3") == Fraction(3, 1)

try:
    Fraction(1, 0)
except ZeroDivisionError:
    pass
else:
    raise AssertionError("Denominator 0 must raise ZeroDivisionError")

try:
    Fraction("3//4")
except ValueError:
    pass
else:
    raise AssertionError("Invalid string format must raise ValueError")

x = Fraction(1,2)
try:
    x.numerator = 10
except AttributeError:
    pass
else:
    raise AssertionError("Immutability broken (numerator changed)")

a, b = Fraction(1,2), Fraction(1,3)
assert a + b == Fraction(5,6)
assert a - 1 == Fraction(-1,2)
assert 1 - a == Fraction(1,2)
assert a * 2 == Fraction(1,1)
assert 3 / a == Fraction(6,1)
try:
    _ = a / 0
except ZeroDivisionError:
    pass
else:
    raise AssertionError("Division by zero must raise ZeroDivisionError")

assert (Fraction(2,3) ** 0) == Fraction(1,1)
assert (Fraction(2,3) ** 3) == Fraction(8,27)
assert (Fraction(2,3) ** -2) == Fraction(9,4)

try:
    Fraction(0,1) ** -1
except ValueError:
    pass
else:
    raise AssertionError("0 to negative power must raise ValueError")

assert Fraction(2,4) == Fraction(1,2)
s = {Fraction(2,4), Fraction(3, 4)}
assert Fraction(1,2) in s
d = {Fraction(2,4): "half"}
assert d[Fraction(1,2)] == "half"

assert Fraction(1,3) < Fraction(1,2)
assert Fraction(-1, 4) < Fraction(0)

f_pos = MixedFraction(7, 3)
f_neg = MixedFraction(-7, 3)
f_pure = MixedFraction(2, 3)
f_whole = MixedFraction(9, 3)

assert str(f_pos) == "2 and 1/3"
assert str(f_neg) == "-2 and 1/3"
assert str(f_pure) == "2/3"
assert str(f_whole) == "3"
