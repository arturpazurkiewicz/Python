#! /usr/bin/python3
import sys


def last_column_adder_from_text(t):
    return sum([int(line.split()[-1]) for line in t.splitlines()])


if __name__ == "__main__":
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
        print("Total bytes:", last_column_adder_from_text(text))
    except IndexError:
        print("Type valid file name")
    except TypeError:
        print("Invalid file")
