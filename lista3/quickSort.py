#! /usr/bin/python3


def quick_sort1(sequence):
    if len(sequence) < 2:
        return sequence
    else:
        pivot = sequence.pop()
        return quick_sort1(list(filter(lambda x: x < pivot, sequence))) + [pivot] + quick_sort1(
            list(filter(lambda x: x >= pivot, sequence)))


def quick_sort2(sequence):
    if len(sequence) < 2:
        return sequence
    else:
        pivot = sequence.pop()
        return quick_sort2([x for x in sequence if x < pivot]) + [pivot] + quick_sort2(
            [x for x in sequence if x >= pivot])


if __name__ == "__main__":
    print(quick_sort1([1, 3, 5, 3, 2, 1, 76, 95, 3, 6]))
    print(quick_sort2([1, 3, 5, 3, 2, 1, 76, 95, 3, 6]))

