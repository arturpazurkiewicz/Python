#!/usr/bin/python3
import random


def tree_generator(height):
    return tree_generator_with_top(height, True)


def tree_generator_with_top(height, top):
    height -= 1
    if 0 <= height:
        if top:
            if random.randint(0, 1) == 1:
                l = tree_generator_with_top(height, False)
                r = tree_generator_with_top(height, True)
                return [random.randint(0, 100), l, r]
            else:
                l = tree_generator_with_top(height, True)
                r = tree_generator_with_top(height, False)
                return [random.randint(0, 100), l, r]
        if random.randint(0, 1) == 1:
            l = tree_generator_with_top(height, 0)
            r = tree_generator_with_top(height, 0)
            return [random.randint(0, 100), l, r]
    return None


def dfs(y):
    for element in y:
        if type(element) == list:
            for i in dfs(element):
                yield i
        else:
            if element is not None:
                yield element


def bfs(x):
    t = [x]
    while len(t) > 0:
        yield t[0][0]
        node = t.pop(0)
        for sub_node in node[1:]:
            if sub_node is not None:
                t.append(sub_node)


if __name__ == "__main__":
    tree = tree_generator(3)
    print(tree)
    print(list(dfs(["1", ["2", ["4", ["8", None, None], ["9", None, None]],
                          ["5", None, None]],
                    ["3", ["6", None, None], ["7", None, None]]])))
    print(list((bfs(["1", ["2", ["4", ["8", None, None], ["9", None, None]],
                           ["5", None, None]],
                     ["3", ["6", None, None], ["7", None, None]]]))))
    print(list((bfs(["1", ["2", ["4", ["8", None, None], ["9", None, None]],
                           ["5", None, None]],
                     ["3", ["6", None, None], ["7", None, None]]]))))
