#! /usr/bin/python3
import os
import sys


def get_info(filename):
    size = os.stat(filename).st_size
    f = open(filename)
    data = f.read()
    lines = data.splitlines()
    max_line = len(max(lines, key=len))
    lines = len(lines)
    words = len(data.split())
    f.close()
    return size, words, lines, max_line


if __name__ == "__main__":
    try:
        size, words, lines, max_line = get_info(sys.argv[1])
        print("Size:", size, "\nNumber of words", words, "\nNumber of lines:", lines, "\nMax line length: ", max_line)
    except (IndexError, FileNotFoundError):
        print("Type valid file name")
