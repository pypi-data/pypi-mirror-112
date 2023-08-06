"""Test suite for mathdunders.py."""

import unittest
from decimal import Decimal
from fractions import Fraction
from math import ceil, floor, trunc
from mathdunders import mathdunders, dunders


@mathdunders()
class r(float):
    """Represents a real number."""


class TestMathDunders(unittest.TestCase):
    def check(self, a, b, a_type=r, b_type=None):
        self.assertEqual(a, b)
        if a_type is not None:
            self.assertEqual(type(a), a_type)
        if b_type is not None:
            self.assertEqual(type(b), b_type)

    # Various Tests:

    def test_lists(self):
        unary = ['__abs__', '__ceil__', '__floor__', '__neg__', '__pos__', '__round__', '__trunc__']
        binary = ['__add__', '__divmod__', '__floordiv__', '__mod__', '__mul__', '__pow__', '__sub__', '__truediv__',
                  '__radd__', '__rdivmod__', '__rfloordiv__', '__rmod__', '__rmul__', '__rpow__', '__rsub__', '__rtruediv__']
        self.assertEqual(sorted(dunders), sorted(unary + binary))

    def test_zero(self):
        self.check(r(), 0)
        self.check(r(), 0.0)
        self.check(r(-0), 0)
        self.check(r(-0.0), -0.0)
        self.check(r(), r())
        self.check(r(), r(0))
        self.check(r(), r(0.0))
        self.check(r(), r("0.0"))

    def test_init(self):
        self.check(r(3.1), 3.1)
        self.check(r(-3.7), r(-3.7))
        self.check(r(3.0), r(3))
        self.check(r("3"), r(3))
        self.check(r("3e-9"), r(3e-9))
        self.check(r(-3), -3)
        self.check(r(1092837675), 1092837675)
        self.check(r(-0.00000017), -0.00000017)
        self.check(r(34e-19), 34e-19)
        with self.assertRaises(TypeError):
            r(1, 2)

    def test_casts(self):
        self.check(str(r(-64)), "-64.0", str)
        self.check(f"{r(5):.03f}", "5.000", str)
        self.check(int(r(-50)), -50, int)
        self.check(float(r(9.8)), 9.8, float)
        self.check(bool(r()), False, bool)
        self.check(bool(r(1)), True, bool)
        self.check(bool(r(0.00001)), True, bool)
        self.check(r(9) < r(10), True, bool)
        self.check(r(90) >= r(10), True, bool)

    def test_i(self):
        x = r(1)
        x += 1
        self.check(x, 2)
        x **= 3
        self.check(x, 8.0)
        x //= 4
        self.check(x, 2)
        x /= .125
        self.check(x, 16)
        x -= 100
        self.check(x, -84)
        x %= 10
        self.check(x, 6)

    def test_int(self):
        @mathdunders()
        class i(int):
            pass
        self.check(i(210), 210, i)
        self.check(i(2.5) + 3, 5, i)
        self.check(2 + i(3.5), 5, i)
        self.check(i(2.5) + i(3.5), 5, i)

    def test_decimal(self):
        @mathdunders()
        class d(Decimal):
            pass
        self.check(d("3e-100"), Decimal("3e-100"), d)
        self.check(d("9e88"), Decimal("9e88"), d)
        self.check(d(2.5) + 3, 5.5, d)
        self.check(2 + d(3.5), 5.5, d)
        self.check(d(2.5) + d(3.5), 6, d)

    def test_complex(self):
        @mathdunders()
        class c(complex):
            pass
        self.check(c(1j), 1j, c)
        self.check(c(2+4j), 2+4j, c)
        self.check(c(2+4j) * (1+2j), -6+8j, c)
        self.check((2+4j) * c(1+2j), -6+8j, c)
        self.check(c(2+4j) * c(1+2j), -6+8j, c)

    def test_rational(self):
        @mathdunders()
        class f(Fraction):
            pass
        self.check(f(1, 2) + f(3, 2), 2, f)
        self.check(0 - f(10) - f() - 1, -11, f)

    def test_force(self):
        @mathdunders(force=True)
        class f(float):
            def __add__(self, other):
                return 123

            def __radd__(self, other):
                return 456

        @mathdunders()
        class g(float):
            def __add__(self, other):
                return 1234

            def __radd__(self, other):
                return 5678

        self.check(f() + f(), 0, f)
        self.check(f() - f(), 0, f)
        self.check(f() + 2, 2, f)
        self.check(2 + f(), 2, f)

        self.check(g() + g(), 1234, int)
        self.check(g() - g(), 0, g)
        self.check(g() + 2, 1234, int)
        self.check(2 + g(), 5678, int)

        self.check(f(4) + g(6), 10, f)
        self.check(g(4) + f(6), 1234, int)

    def test_base(self):
        @mathdunders(float)
        class b(float):
            pass
        self.check(float(b(1.1)), 1.1, float)
        self.check(int(b(1)), 1, int)
        self.check(b(9) + 8, 17, b)
        self.check(8 + b(9), 17, b)
        self.check(b(8) + b(9), 17, b)

    def test_multibase(self):
        class p:
            pass

        @mathdunders()
        class b(float, p):
            pass
        self.check(float(b(1.1)), 1.1, float)
        self.check(int(b(1)), 1, int)
        self.check(b(9) + 8, 17, b)
        self.check(8 + b(9), 17, b)
        self.check(b(8) + b(9), 17, b)

        @mathdunders(base=float)
        class b(p, float):
            pass
        self.check(float(b(1.1)), 1.1, float)
        self.check(int(b(1)), 1, int)
        self.check(b(9) + 8, 17, b)
        self.check(8 + b(9), 17, b)
        self.check(b(8) + b(9), 17, b)

        with self.assertRaises(Exception):
            @mathdunders()
            class e(p, float):
                pass

    def test_custom_dunders(self):
        @mathdunders(dunders=['__add__', '__and__'])
        class d(int):
            pass
        self.check(d(4) + d(5), 9, d)
        self.check(d(4) + 5, 9, d)
        self.check(4 + d(5), 9, int)

        self.check(d(7) - d(9), -2, int)
        self.check(d(7) - 9, -2, int)
        self.check(7 - d(9), -2, int)

        self.check(d(2) & d(3), 2, d)
        self.check(d(2) & 3, 2, d)
        self.check(2 & d(3), 2, int)

    # Unary Dunder Tests:

    def test_abs(self):
        self.check(abs(r(0)), 0)
        self.check(abs(r(4)), 4)
        self.check(abs(r(-4)), 4)

    def test_ceil(self):  # Will fail in < 3.9.
        self.check(ceil(r(1.5)), 2)
        self.check(ceil(r(-1.5)), -1)

    def test_floor(self):  # Will fail in < 3.9.
        self.check(floor(r(1.5)), 1)
        self.check(floor(r(-1.5)), -2)

    def test_neg(self):
        self.check(-r(0), 0)
        self.check(-r(4), -4)
        self.check(-r(-4), 4)

    def test_pos(self):
        self.check(+r(0), 0)
        self.check(+r(4), 4)
        self.check(+r(-4), -4)

    def test_round(self):
        self.check(round(r(1.5)), 2)
        self.check(round(r(-1.5)), -2)
        self.check(round(r(2.5)), 2)
        self.check(round(r(-2.5)), -2)
        self.check(round(r(9.1)), 9)
        self.check(round(r(-9.1)), -9)
        self.check(round(r(9.9)), 10)
        self.check(round(r(-9.9)), -10)

    def test_trunc(self):
        self.check(trunc(r(1.5)), 1)
        self.check(trunc(r(-1.5)), -1)
        self.check(trunc(r(2.5)), 2)
        self.check(trunc(r(-2.5)), -2)
        self.check(trunc(r(9.1)), 9)
        self.check(trunc(r(-9.1)), -9)
        self.check(trunc(r(9.9)), 9)
        self.check(trunc(r(-9.9)), -9)

    # Binary Dunder Tests:

    def test_add(self):
        self.check(r(0) + 0, 0)
        self.check(r(0) + r(0), 0)
        self.check(r(1) + 1, 2)
        self.check(r(1) + 1.0, 2)
        self.check(r(1) + r(1), 2)
        self.check(1 + r(1), 2)
        self.check(r(1) + r(1), 2)
        self.check(r(1) + 3 + r(1), 5)
        self.check(1 + r(3) + 1, 5)

    def test_divmod(self):
        self.check(divmod(r(17), 3), (5, 2), tuple)
        self.check(divmod(r(17), 3)[0], 5)
        self.check(divmod(r(17), 3)[1], 2)
        self.check(divmod(17, r(3))[0], 5)
        self.check(divmod(17, r(3))[1], 2)
        self.check(divmod(r(17), r(3))[0], 5)
        self.check(divmod(r(17), r(3))[1], 2)

    def test_floordiv(self):
        self.check(r(11) // 2, 5)
        self.check(r(11) // 2.0, 5)
        self.check(11 // r(2), 5)
        self.check(11 // r(2.0), 5)
        self.check(r(11) // r(2), 5)
        self.check(r(11) // r(2.0), 5)
        with self.assertRaises(ZeroDivisionError):
            r(0) // 0
        with self.assertRaises(ZeroDivisionError):
            0 // r(0)
        with self.assertRaises(ZeroDivisionError):
            r(0) // r(0)

    def test_mod(self):
        self.check(r(9) % 4, 1)
        self.check(r(1.5) % .5, 0)
        self.check(9 % r(4), 1)
        self.check(1.5 % r(.5), 0)
        self.check(r(9) % r(4), 1)
        self.check(r(1.5) % r(.5), 0)

    def test_mul(self):
        self.check(r(3) * 4, 12)
        self.check(3 * r(4), 12)
        self.check(r(3) * r(4), 12)

    def test_pow(self):
        self.check(r(2) ** 3, 8)
        self.check(2 ** r(3), 8)
        self.check(r(2) ** r(3), 8)
        self.check(r(0)**0, 1)

        @mathdunders()
        class i(int):
            pass

        self.check(pow(i(2), 10, 100), 24, i)
        self.check(pow(i(2), i(10), 100), 24, i)
        self.check(pow(i(2), i(10), i(100)), 24, i)
        self.check(pow(2, i(10)), 1024, i)
        self.check(pow(2, i(10), 100), 24, int)  # not exactly sure why int instead of i

    def test_sub(self):
        self.check(r(5) - 7, -2)
        self.check(r(5) - r(7), -2)
        self.check(5 - r(7), -2)

    def test_truediv(self):
        self.check(r(11) / 2, 5.5)
        self.check(r(11) / 2.0, 5.5)
        self.check(11 / r(2), 5.5)
        self.check(11 / r(2.0), 5.5)
        self.check(r(11) / r(2), 5.5)
        self.check(r(11) / r(2.0), 5.5)
        with self.assertRaises(ZeroDivisionError):
            r(0) / 0
        with self.assertRaises(ZeroDivisionError):
            0 / r(0)
        with self.assertRaises(ZeroDivisionError):
            r(0) / r(0)


def test():
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass


if __name__ == "__main__":
    test()
