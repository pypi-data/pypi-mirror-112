# mathdunders

**A Python decorator that automatically adds math-related dunder methods to a class derived from a numeric type.**

Useful when you want operations on that class to remain the same type but don't want to manually write all the dunders.

Think of it in the same vein as [@functools.total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering).

## Installation

```text
pip install mathdunders
```

[View on PyPI](https://pypi.org/project/mathdunders/) - [View on GitHub](https://github.com/discretegames/mathdunders)

This package was built in Python 3.9.4 and tested to work in 3.6.8+.

## Usage

Import and put `@mathdunders()` above your class:

```py
from mathdunders import mathdunders

@mathdunders()
class RealNumber(float):
    pass

a = RealNumber(3) + RealNumber(4)
print(a, type(a))  # -> 7.0 <class '__main__.RealNumber'>

b = RealNumber(3) * 4
print(b, type(b))  # -> 12.0 <class '__main__.RealNumber'>

c = 3 - RealNumber(4)
print(c, type(c))  # -> -1.0 <class '__main__.RealNumber'>
```

Now any math operation with `RealNumber` will result in another `RealNumber` rather than a float.

In the above code block, `@mathdunders()` makes `RealNumber` behave as if it was written like:

```py
class RealNumber(float):
    def __add__(self, other):
        return RealNumber(float(self) + other)

    def __mul__(self, other):
        return RealNumber(float(self) * other)

    def __rsub__(self, other):
        return RealNumber(other - float(self))

    # ... plus 20 other similar boilerplate dunder methods ...
```

## Supported Dunders

`@mathdunders()` adds 23 "magic" double-underscore (dunder) methods to the class it decorates:

```text
Dunder           Trigger
__abs__          abs(x)
__ceil__         math.ceil(x)
__floor__        math.floor(x)
__neg__          -x
__pos__          +x
__round__        round(x)
__trunc__        math.trunc(x)
__add__          x + 3
__divmod__       divmod(x, 3)
__floordiv__     x // 3
__mod__          x % 3
__mul__          x * 3
__pow__          x ** 3
__sub__          x - 3
__truediv__      x / 3
__radd__         3 + x
__rdivmod__      divmod(3, x)
__rfloordiv__    3 // x
__rmod__         3 % x
__rmul__         3 * x
__rpow__         3 ** x
__rsub__         3 - x
__rtruediv__     3 / x
```

`dunders` is a tuple of all supported dunder names:

```py
from mathdunders import dunders
print(dunders)  # -> ('__abs__', '__ceil__', '__floor__', '__neg__', ...
```

Comparison operators are omitted because it doesn't make sense for them to return the decorated type.

Bitwise operators are omitted because they are not well defined for many numeric types, e.g. floats.

Note that `__ceil__` and `__floor__` are unimplemented for floats in Python versions before 3.9.

## Advanced Usage

If the base type such as `float`, `int`, or `Decimal` is not the first base class, use the optional `base` parameter to specify it.

```py
from mathdunders import mathdunders

class Parent:
    pass

@mathdunders(base=int)
class Int(Parent, int):
    pass

print(Int(10) / Int(2))  # -> 5
```

---

If you wish to supply a custom set of dunders you may use the optional `dunders` parameter.

```py
from mathdunders import mathdunders, dunders

extras = ('__and__', '__lshift__')
@mathdunders(dunders=dunders + extras)
class Int(int):
    pass

a = Int(2) & Int(3)
print(a, type(a))  # -> 2 <class '__main__.Int'>

b = Int(2) | Int(3)
print(b, type(b))  # -> 3 <class 'int'>

c = Int(1) << 4
print(c, type(c))  # -> 16 <class '__main__.Int'>
```

---

By default dunders are not inserted if the class already defines them. Set the optional parameter `force` to `True` to override this.

```py
from mathdunders import mathdunders

@mathdunders(force=False)  # default behavior
class A(float):
    def __abs__(self):
        return 1234

a = abs(A(-1))
print(a, type(a))  # -> 1234 <class 'int'>

@mathdunders(force=True)  # forces dunders to be overwritten
class B(float):
    def __abs__(self):
        return 1234

b = abs(B(-1))
print(b, type(b))  # -> 1.0 <class '__main__.B'>
```

---
