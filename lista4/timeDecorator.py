#!/usr/bin/python3

import time


def measure_time(function):
    def modified_function(*args, **kwargs):
        start = time.time()
        r = function(*args, **kwargs)
        timing = time.time() - start
        print("Measured time", timing)
        return r

    return modified_function


def powerset(lst):
    return [[lst[j] for j in range(len(lst)) if (x & (1 << j))] for x in
            range(1 << len(lst))]


if __name__ == "__main__":
    f = measure_time(powerset)
    print(f([1, 2, 3, 4]))
