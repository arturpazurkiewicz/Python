#! /usr/bin/python3
def flatten(l):
    for element in l:
        if type(element) == list:
            for i in flatten(element):
                yield i
        else:
            yield element


if __name__ == "__main__":
    l = [[1, 2, ["a", 4, "b", 5, 5, 5]], [4, 5, 6], 7, [[9, [123, [[123]]]], 10]]
    a = flatten(l)
    print(a)
    for i in a:
        print(i)
    print(list(flatten(l)))
