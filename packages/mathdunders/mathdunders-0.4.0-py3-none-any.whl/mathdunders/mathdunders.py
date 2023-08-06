"""This module provides a decororator that automatically adds math dunder methods to a class."""

unary = "abs ceil floor neg pos round trunc".split()
binary = "add divmod floordiv mod mul pow sub truediv".split()
binary = binary + [f"r{name}" for name in binary]
dunders = tuple(f"__{name}__" for name in unary + binary)


def mathdunders(base=None, dunders=dunders, force=False):
    """Decorator that automatically adds math dunders to a class."""

    def decorator(cls):
        nonlocal base
        if base is None:
            base = cls.__bases__[0]

        def make_dunder(name):  # Needed to encapsulate name.
            def dunder(self, *args):
                result = getattr(base(self), name)(*args)
                if result is NotImplemented:
                    return NotImplemented
                if type(result) is tuple:  # Exact type check intentional.
                    return tuple(map(cls, result))  # Only divmod and rdivmod return tuples.
                return cls(result)
            return dunder

        for name in dunders:
            cls_has = hasattr(cls, name) and getattr(cls, name) is not getattr(base, name)
            if force or not cls_has:
                setattr(cls, name, make_dunder(name))

        return cls
    return decorator
