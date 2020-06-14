#! /usr/bin/python3
from functools import reduce


def powerset1(lst):
    return [[lst[j] for j in range(len(lst)) if (x & (1 << j))] for x in range(1 << len(lst))]


def powerset2(lst):
    return list(map(lambda x: list(map(lambda y: lst[y], filter(lambda j: x & (1 << j), range(len(lst))))),
                    range(1 << len(lst))))


def powerset3(lst):
    return reduce(lambda result, x: result + list(map(lambda subset: subset + [x], result)), lst, [[]])


if __name__ == "__main__":
    print(powerset1(["a", "b", "c"]))
    print(powerset2(["a", "b", "c"]))
    print(powerset2(["a", "b", "c"]))
