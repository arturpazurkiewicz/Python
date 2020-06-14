#!/usr/bin/python3
import math
from inspect import getfullargspec


def overload(func):
    OverloadedFunction.registry[
        (func.__name__, len(getfullargspec(func).args))] = func

    def overrider(*args, **kwargs):
        return OverloadedFunction(func.__name__)(*args, **kwargs)

    return overrider


class OverloadedFunction:
    registry = {}

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        s = args.__len__() + kwargs.__len__()
        n = self.name
        f = OverloadedFunction.registry.get((n, s))

        if f is None:
            raise TypeError("Invalid arguments")

        return f(*args, **kwargs)


@overload
def norm(x, y):
    return math.sqrt(x * x + y * y)


@overload
def norm(x, y, z):
    return abs(x) + abs(y) + abs(z)


if __name__ == "__main__":
    print(f"norm(2,4) = {norm(2, 4)}")

    print(f"norm(2,3,4) = {norm(2, 3, 4)}")
