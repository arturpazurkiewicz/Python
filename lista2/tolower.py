#! /usr/bin/python3
import os
import sys


def to_lower(dir):
    dir = os.path.join(os.getcwd(),dir)
    dir_list = os.listdir(dir)

    for x in dir_list:
        pom = os.path.join(dir, x)
        if os.path.isdir(pom):
            to_lower(os.path.join(dir, x))
        os.rename(pom,os.path.join(dir, x.lower()))


if __name__ == "__main__":
    try:
        to_lower(sys.argv[1])

    except (IndexError, FileNotFoundError):
        print("Type valid directory")
