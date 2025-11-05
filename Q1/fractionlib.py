import math
from functools import total_ordering

def _gcd(a, b):
    return math.gcd(a, b)

@total_ordering
class Fraction:
    __slots__ = ("_numerator", "_denominator")
    def __init__(self, numerator, denominator=None):
        if isinstance(numerator, str):
            if denominator is not None:
                raise TypeError("Cannot provide denominator with string input")
            self._parse_string(numerator)
        elif isinstance(numerator, int):
            if denominator is None:
                denominator = 1
            if not isinstance(denominator, int):
                raise TypeError("Denominator must be an integer")
            self._set_values(numerator, denominator)
        elif isinstance(numerator, Fraction):
            if denominator is not None:
                raise TypeError("Cannot provide denominator when copying Fraction")
            self._set_values(numerator.numerator, numerator.denominator)
        else:
            raise TypeError("Numerator must be an integer, string, or Fraction")

    def __setattr__(self, name, value):
        raise AttributeError(f"{self.__class__.__name__} instances are immutable")

    def _set_values(self, num, den):
        if den == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        common = _gcd(abs(num), abs(den))
        num //= common
        den //= common
        if den < 0:
            num, den = -num, -den
        object.__setattr__(self, "_numerator", num)
        object.__setattr__(self, "_denominator", den)

    def _parse_string(self, s):
        s = s.strip()
        if '/' in s:
            parts = s.split('/')
            if len(parts) != 2:
                raise ValueError(f"Invalid fraction string: {s}")
            try:
                num = int(parts[0].strip())
                den = int(parts[1].strip())
            except ValueError:
                raise ValueError(f"Invalid fraction string: {s}")
            self._set_values(num, den)
        else:
            try:
                num = int(s)
            except ValueError:
                raise ValueError(f"Invalid fraction string: {s}")
            self._set_values(num, 1)

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    def _coerce(self, other):
        if isinstance(other, int):
            return Fraction(other, 1)
        if isinstance(other, Fraction):
            return other
        return NotImplemented

    def __add__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        num = self._numerator * other._denominator + other._numerator * self._denominator
        den = self._denominator * other._denominator
        return self.__class__(num, den)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        num = self._numerator * other._denominator - other._numerator * self._denominator
        den = self._denominator * other._denominator
        return self.__class__(num, den)

    def __rsub__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        num = self._numerator * other._numerator
        den = self._denominator * other._denominator
        return self.__class__(num, den)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        if other._numerator == 0:
            raise ZeroDivisionError("Division by zero")
        num = self._numerator * other._denominator
        den = self._denominator * other._numerator
        return self.__class__(num, den)

    def __rtruediv__(self, other):
        if isinstance(other, int):
            if self._numerator == 0:
                raise ZeroDivisionError("Division by zero")
            return Fraction(other * self._denominator, self._numerator)
        if isinstance(other, Fraction):
            return other.__truediv__(self)
        raise TypeError("Unsupported type for right-division")

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise TypeError("Exponent must be an integer")
        if exponent == 0:
            return self.__class__(1, 1)
        if exponent < 0:
            if self._numerator == 0:
                raise ValueError("Cannot raise zero to a negative power")
            return (self.__class__(self._denominator, self._numerator) ** (-exponent))
        return self.__class__(self._numerator ** exponent, self._denominator ** exponent)

    def __neg__(self):
        return self.__class__(-self._numerator, self._denominator)

    def __abs__(self):
        return self.__class__(abs(self._numerator), self._denominator)

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __ipow__(self, other):
        return self.__pow__(other)

    def __eq__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return False
        return self._numerator == other._numerator and self._denominator == other._denominator

    def __lt__(self, other):
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self._numerator * other._denominator < other._numerator * self._denominator

    def __hash__(self):
        return hash((self._numerator, self._denominator))

    def __float__(self):
        return self._numerator / self._denominator

    def __int__(self):
        return int(self._numerator / self._denominator)

    def __str__(self):
        if self._denominator == 1:
            return str(self._numerator)
        return f"{self._numerator}/{self._denominator}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._numerator}, {self._denominator})"

class MixedFraction(Fraction):
    def __str__(self):
        if self._denominator == 1:
            return str(self._numerator)
        whole = int(self._numerator / self._denominator)
        rem = abs(self._numerator) - abs(whole) * self._denominator
        if rem == 0:
            return str(whole)
        if whole == 0:
            return f"{self._numerator}/{self._denominator}"
        return f"{whole} and {rem}/{self._denominator}"