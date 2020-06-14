#!/usr/bin/python3
import random


class Node:
    def __init__(self, value):
        self.value = value
        self.sub_node = []

    def add_node(self, node):
        if node is not None:
            self.sub_node.append(node)

    def dfs(self):
        yield self.value
        for node in self.sub_node:
            for i in node.dfs():
                yield i

    def bfs(self):
        t = [self]
        while len(t) > 0:
            yield t[0].value
            node = t.pop(0)
            for sub in node.sub_node:
                t.append(sub)


def tree_generator(height, max_sub_node):
    return tree_generator_with_top(height, True, max_sub_node)


def tree_generator_with_top(height, top, max_sub_node):
    height -= 1
    if 0 <= height:
        node = Node(random.randint(0, 100))
        if top:
            all_options = random.randint(1, max_sub_node)
            chosen = random.randint(0, all_options - 1)
            for i in range(all_options):
                if chosen == i:
                    node.add_node(
                        tree_generator_with_top(height, True, max_sub_node))
                else:
                    node.add_node(
                        tree_generator_with_top(height, False, max_sub_node))
        else:
            if random.randint(0, 1) == 1:
                all_options = random.randint(1, max_sub_node)
                for i in range(all_options):
                    node.add_node(
                        tree_generator_with_top(height, False, max_sub_node))
        return node
    else:
        return None


if __name__ == "__main__":
    t = tree_generator(4, 4)
    dfs = list(t.dfs())
    print(dfs)
    bfs = list(t.bfs())
    print(bfs)
